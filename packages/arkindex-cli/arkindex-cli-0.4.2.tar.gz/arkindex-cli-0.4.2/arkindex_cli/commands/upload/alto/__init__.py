# -*- coding: utf-8 -*-
import csv
import errno
import itertools
import logging
import re
from itertools import filterfalse
from operator import itemgetter
from pathlib import Path
from typing import List, Optional, Union
from uuid import UUID

from apistar.exceptions import ErrorResponse
from lxml import etree as ET
from lxml import objectify
from requests.compat import quote
from rich.progress import Progress, track

from arkindex_cli.argtypes import URLArgument
from arkindex_cli.auth import Profiles
from arkindex_cli.client import ArkindexAPIClient
from arkindex_cli.commands.upload.alto.parser import (
    AltoElement,
    AltoMetadata,
    RootAltoElement,
)
from arkindex_cli.commands.upload.cache import Cache, save_cache
from arkindex_cli.commands.upload.exceptions import UploadProcessingError

REGEX_IMAGE_ID = re.compile(r"0+(\d+)")
REGEX_METADATA_ERROR = re.compile(
    r"Metadata ({.*}) already exist\(s\) on this element\."
)

logger = logging.getLogger(__name__)


def add_alto_arguments(parser):
    parser.add_argument(
        "--alto-namespace",
        help="Specify an Alto namespace to use.",
        required=False,
        type=str,
    )
    parser.add_argument(
        "path",
        help="Path to a directory which contains ALTO XML documents. Defaults to the current working directory.",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--iiif-base-url",
        help="Base URL for the IIIF images, which will be prepended to all source image file names.",
        type=URLArgument(allow_query=False),
        required=True,
    )
    parser.add_argument(
        "--parent-id",
        help="UUID of a parent folder under which page elements will be created.",
        type=UUID,
        required=True,
    )
    parser.add_argument(
        "--skip-metadata",
        help="Skipping ALTO metadata publication, speeds up a lot the execution time",
        action="store_true",
    )
    parser.add_argument(
        "--worker-run-id",
        help="Worker Run used to publish elements, transcriptions and metadata in bulk.",
        type=UUID,
        required=True,
    )
    parser.add_argument(
        "--dpi-x",
        help="Horizontal resolution of the image, in dots per inch, to be used for ALTO files using coordinates in tenths of millimeters.\n"
        "Strictly positive integer. Ignored for files using coordinates in pixels.",
        type=int,
    )
    parser.add_argument(
        "--dpi-y",
        help="Vertical resolution of the image, in dots per inch, to be used for ALTO files using coordinates in tenths of millimeters.\n"
        "Strictly positive integer. Ignored for files using coordinates in pixels.",
        type=int,
    )
    types = parser.add_mutually_exclusive_group(required=True)
    types.add_argument(
        "--create-types",
        help="Create an element type in the Arkindex corpus for each element type in the ALTO files.",
        action="store_true",
    )
    types.add_argument(
        "--existing-types",
        help='Specify correspondences between element types in the Arkindex corpus and in the ALTO files. Format: --existing-types="alto_type:arkindex_type alto_type_2:arkindex_type_2"',
        type=str,
    )


def add_alto_parser(subcommands):
    # Gallica parser
    gallica = subcommands.add_parser(
        "gallica",
        help="The images are on Gallica IIIF server.",
    )
    gallica.add_argument(
        "--metadata-file",
        help="CSV that contains the metadata related to the Gallica import.",
        required=True,
        type=Path,
    )
    add_alto_arguments(gallica)
    gallica.set_defaults(func=run_gallica)

    # Generic Alto parser
    alto = subcommands.add_parser(
        "alto",
        description="Upload ALTO XML documents to Arkindex.",
        help="Upload ALTO XML documents to Arkindex.",
    )
    add_alto_arguments(alto)
    alto.set_defaults(func=run)


def check_element_type(corpus: dict, type_slug: str) -> None:
    types = {type["slug"] for type in corpus["types"]}
    if type_slug not in types:
        logger.error(f"Type {type_slug} not found.")
        raise UploadProcessingError


def create_iiif_image(client: ArkindexAPIClient, url: str) -> str:
    logger.debug(f"Creating image from URL {url}…")
    try:
        image = client.request("CreateIIIFURL", body={"url": url})
        return image["id"]
    except ErrorResponse as e:
        # When the image already exists, its ID is returned in a HTTP 400
        if e.status_code == 400 and "id" in e.content:
            return e.content["id"]
        logger.error(
            f"Failed to create image from target URL {url}: {e.status_code} - {e.content}"
        )
        raise UploadProcessingError


_TYPES = {}


def get_element_type(
    client: ArkindexAPIClient,
    corpus_id: UUID,
    node_name: str,
    types_dict: Optional[dict],
    create_types: bool = False,
):
    """
    Retrieve or create an alto node's corresponding Arkindex element type.
    Always fetch types from Arkindex if not cached yet.
    If types_dict is set, directly look for a matching type from that dictionary.
    Otherwise, look for a matching Arkindex type, creating it if required.
    """
    corpus_id = str(corpus_id)
    if corpus_id not in _TYPES:
        _TYPES[corpus_id] = arkindex_corpus_types = [
            item["slug"]
            for item in client.request("RetrieveCorpus", id=corpus_id)["types"]
        ]
    else:
        arkindex_corpus_types = _TYPES[corpus_id]

    if types_dict is None and not create_types:
        logger.error(
            f"No type can be found matching node {node_name} in corpus {corpus_id}. "
            "Hint: either define types_dict or allow type creation."
        )
        raise UploadProcessingError

    if types_dict is not None:
        if node_name not in types_dict:
            logger.error(f"Alto element {node_name} not in given types dictionary.")
            raise UploadProcessingError
        return types_dict[node_name]

    if node_name in arkindex_corpus_types:
        logger.debug(f"Element type {node_name} exists in target corpus {corpus_id}.")
    else:
        logger.debug(f"Creating element type {node_name} in target corpus {corpus_id}…")

        try:
            client.request(
                "CreateElementType",
                body={
                    "slug": node_name,
                    "display_name": node_name,
                    "corpus": corpus_id,
                },
            )
            _TYPES[corpus_id].append(node_name)
        except ErrorResponse as e:
            logger.error(
                f"Failed to create element type {node_name} in target corpus {corpus_id}: {e.status_code} - {e.content}."
            )
            raise UploadProcessingError

    return node_name


def create_metadata(
    client: ArkindexAPIClient,
    element_id: str,
    metadata_list: list[dict],
    worker_run_id: UUID,
    reraise: bool = False,
) -> None:
    if not metadata_list:
        return

    try:
        client.request(
            "CreateMetaDataBulk",
            id=element_id,
            body={
                "worker_run_id": str(worker_run_id),
                "metadata_list": metadata_list,
            },
        )
        logger.debug(f"Published {len(metadata_list)} metadata")
    except ErrorResponse as e:
        # Check if all metadata already exist
        content = REGEX_METADATA_ERROR.fullmatch(
            e.content.get("non_field_errors", [""])[0]
        )
        if (
            reraise
            or e.status_code != 400
            or len(e.content.get("non_field_errors", [])) != 1
            or not content
        ):
            logger.error(
                f"Failed to create metadata on target element {element_id}: {e.status_code} - {e.content}."
            )
            raise UploadProcessingError

        # Ignore existing metadata
        existing_metadatas = eval(content.group(1))
        if len(metadata_list) == len(existing_metadatas):
            return

        # Try to publish missing metadata only
        metadata_list = [
            metadata
            for metadata in metadata_list
            if (metadata["name"], metadata["type"], metadata["value"])
            not in existing_metadatas
        ]
        create_metadata(client, element_id, metadata_list, worker_run_id, reraise=True)


def create_element_parent(
    client: ArkindexAPIClient,
    parent_id: str,
    child_id: str,
) -> None:
    logger.debug(f"Linking element {child_id} to parent {parent_id}…")
    try:
        client.request(
            "CreateElementParent",
            parent=parent_id,
            child=child_id,
        )
    except ErrorResponse as e:
        # Ignore "already" errors
        if e.status_code != 400 or all(
            "is already a parent of" not in message
            for message in e.content.get("parent", [])
        ):
            logger.error(
                f"Failed to link target element {child_id} to parent {parent_id}: {e.status_code} - {e.content}."
            )
            raise UploadProcessingError


def create_element_parents(
    client: ArkindexAPIClient,
    nodes: List[AltoElement],
    parent_id: UUID,
    cache: Cache,
) -> None:
    if not nodes:
        return

    # List children to link only the missing ones
    try:
        child_ids = set(
            map(itemgetter("id"), client.paginate("ListElementChildren", id=parent_id))
        )
    except ErrorResponse as e:
        logger.error(
            f"Failed to retrieve children of target element {parent_id}: {e.status_code} - {e.content}"
        )
        raise UploadProcessingError

    for node in nodes:
        # Check if the child is already linked to the parent
        arkindex_id = cache.get(node.id)
        if arkindex_id in child_ids:
            continue
        create_element_parent(client, parent_id, child_id=arkindex_id)


@save_cache
def create_elements(
    client: ArkindexAPIClient,
    nodes: List[AltoElement],
    image_id: str,
    parent_id: UUID,
    corpus_id: str,
    worker_run_id: UUID,
    cache: Cache,
    parent_node: Union[AltoElement, None] = None,
    publish_metadata: bool = True,
    create_types: bool = True,
    types_dict: Optional[dict] = None,
    metadata_list: Optional[list[AltoMetadata]] = [],
) -> None:
    # Update node's metadata before publishing them
    if publish_metadata and metadata_list:
        for node in nodes:
            for alto_metadata in metadata_list:
                node.metadata_list.extend(alto_metadata.get_metadata_list(node.content))

    # Cleanup nodes:
    # - no nodes without ID
    # - no nodes without polygon when parent has a polygon
    cleaned_nodes = [
        node for node in nodes if node.id and (parent_node is None or node.polygon)
    ]
    if not cleaned_nodes:
        # Do not create this node but iterate on their children
        for node in nodes:
            if not node.children:
                continue

            create_elements(
                client,
                nodes=node.children,
                image_id=image_id,
                parent_id=parent_id,
                corpus_id=corpus_id,
                worker_run_id=worker_run_id,
                cache=cache,
                parent_node=node,
                publish_metadata=publish_metadata,
                types_dict=types_dict,
                create_types=create_types,
                metadata_list=metadata_list,
            )

    def in_cache(node: AltoElement) -> bool:
        return cache.get(node.id)

    missing_nodes = list(filterfalse(in_cache, cleaned_nodes))
    existing_nodes = list(filter(in_cache, cleaned_nodes))

    # Try to link every existing nodes to the parent
    create_element_parents(client, existing_nodes, parent_id, cache)

    # Create elements slowly one-by-one when
    # - parent is unknown, so probably without any polygon nor image
    # - parent is known but has not polygon
    # - all nodes without any zones
    distinctive_elts = (
        missing_nodes
        if parent_node is None or not parent_node.polygon
        else [node for node in missing_nodes if not node.polygon]
    )

    for node in distinctive_elts:
        body = {
            "corpus": corpus_id,
            "parent": str(parent_id),
            "type": get_element_type(
                client,
                corpus_id,
                node.node_name,
                types_dict=types_dict,
                create_types=create_types,
            ),
            "name": node.name,
            "worker_run_id": str(worker_run_id),
        }

        if image_id and node.polygon:
            body["polygon"] = node.polygon
            body["image"] = image_id

        try:
            element_id = client.request(
                "CreateElement",
                body=body,
            )["id"]
        except ErrorResponse as e:
            logger.error(
                f"Failed to create element on target parent {body['parent']}: {e.status_code} - {e.content}."
            )
            raise UploadProcessingError

        # Build transcription when available
        if node.text:
            try:
                client.request(
                    "CreateTranscription",
                    id=element_id,
                    body={
                        "text": node.text,
                        "confidence": node.confidence,
                        "worker_run_id": str(worker_run_id),
                    },
                )
            except ErrorResponse as e:
                logger.error(
                    f"Failed to create transcription on target element {element_id}: {e.status_code} - {e.content}."
                )
                raise UploadProcessingError

        # Store the arkindex ID of the newly created element
        cache.set(node.id, element_id)

    if distinctive_elts:
        logger.debug(f"Published {len(distinctive_elts)} elements distinctly")

    # Split remaining nodes with/without transcriptions
    # to take advantage of CreateElements & CreateElementTranscriptions
    missing_nodes = list(
        filter(lambda node: node not in distinctive_elts, missing_nodes)
    )
    with_transcriptions = [node for node in missing_nodes if node.text]
    without_transcriptions = [node for node in missing_nodes if not node.text]

    if without_transcriptions:
        try:
            elements = client.request(
                "CreateElements",
                id=parent_id,
                body={
                    "worker_run_id": str(worker_run_id),
                    "elements": [
                        {
                            "name": node.name,
                            "type": get_element_type(
                                client,
                                corpus_id,
                                node.node_name,
                                types_dict=types_dict,
                                create_types=create_types,
                            ),
                            "polygon": node.polygon,
                        }
                        for node in without_transcriptions
                    ],
                },
            )
        except ErrorResponse as e:
            logger.error(
                f"Failed to create elements on target parent {parent_id}: {e.status_code} - {e.content}"
            )
            raise UploadProcessingError

        # Store the arkindex ID of the newly created element
        node_ids = (node.id for node in without_transcriptions)
        arkindex_ids = (elt["id"] for elt in elements)
        for node_id, arkindex_id in zip(node_ids, arkindex_ids):
            cache.set(node_id, arkindex_id)

        logger.debug(f"Published {len(without_transcriptions)} elements")

    if with_transcriptions:

        # To create elements and transcriptions, we first
        # need to group nodes by their types
        groups = itertools.groupby(
            sorted(with_transcriptions, key=lambda n: n.node_name),
            lambda n: n.node_name,
        )

        for node_name, node_group in groups:
            node_group = list(node_group)  # needed because we access it several times
            try:
                elements = client.request(
                    "CreateElementTranscriptions",
                    id=parent_id,
                    body={
                        "element_type": get_element_type(
                            client,
                            corpus_id,
                            node_name,
                            types_dict=types_dict,
                            create_types=create_types,
                        ),
                        "worker_run_id": str(worker_run_id),
                        "return_elements": True,
                        "transcriptions": [
                            {
                                "polygon": node.polygon,
                                "text": node.text,
                                "confidence": node.confidence,
                            }
                            for node in node_group
                        ],
                    },
                )
            except ErrorResponse as e:
                logger.error(
                    f"Failed to create elements with transcriptions on target element {parent_id}: {e.status_code} - {e.content}"
                )
                raise UploadProcessingError

            # Store the arkindex ID of the newly created element
            node_ids = (node.id for node in node_group)
            arkindex_ids = (elt["element_id"] for elt in elements)
            for node_id, arkindex_id in zip(node_ids, arkindex_ids):
                cache.set(node_id, arkindex_id)

        logger.debug(
            f"Published {len(with_transcriptions)} elements with transcriptions"
        )

    # Publish metadata
    if publish_metadata:
        for node in cleaned_nodes:
            create_metadata(
                client, cache.get(node.id), node.metadata_list, worker_run_id
            )

    # All nodes are created at this point
    # we can directly iterate on their children
    for node in cleaned_nodes:
        if not node.children:
            continue

        create_elements(
            client,
            nodes=node.children,
            image_id=image_id,
            parent_id=cache.get(node.id),
            corpus_id=corpus_id,
            worker_run_id=worker_run_id,
            cache=cache,
            parent_node=node,
            publish_metadata=publish_metadata,
            types_dict=types_dict,
            create_types=create_types,
            metadata_list=metadata_list,
        )


def format_url(path: Path, iiif_base_url: str, folders_ark_id_dict: dict = None):
    """
    This function is used to create the url to get the image from the Gallica IIIF server
    """
    # The path.name looks like 18840615_1-0003.xml with the folder id being the 18840615 which we use to
    # find the ark_id in order to get the folder from the Gallica server in this case it is ark:/12148/bpt6k7155522
    # the image id is 3 which we add to the url to get the image within the folder on Gallica so this gives us ark:/12148/bpt6k7155522/f3
    # the final link will be http://gallica.bnf.fr/iiif/ark:/12148/bpt6k7155522/f1
    if "-" in path.name:
        basename = path.name.split("-")[1]
        file_extension = path.name.split("-")[0]
        folder_id = file_extension.split("_")[0]
    else:
        # path looks like <folder_id>/ocr/image_id.xml
        folder_id = str(path).split(sep="/")[0]
        basename = path.name
    image_id = basename.replace(".xml", "")
    ark_id = folders_ark_id_dict[folder_id]
    return f"{iiif_base_url}{ark_id}/f{parse_image_idx(image_id)}"


def parse_image_idx(image_id):
    # Remove leading 0s
    image_idx = REGEX_IMAGE_ID.search(image_id)
    if not image_idx:
        logger.error(f"Could not parse the image IDX from `{image_id}`")
        raise UploadProcessingError
    return image_idx.group(1)


def upload_alto_file(
    path: Path,
    client: ArkindexAPIClient,
    iiif_base_url: str,
    corpus: dict,
    parent_id: UUID,
    types_dict: Optional[dict],
    create_types: bool,
    worker_run_id: UUID,
    dpi_x: Optional[int] = None,
    dpi_y: Optional[int] = None,
    gallica: bool = False,
    folders_ark_id_dict: dict = None,
    alto_namespace: str = None,
    skip_metadata: bool = False,
) -> None:
    logger.info(f"Publishing ALTO file @ {path}…")

    # Setup cache next to alto file
    cache = Cache(path.with_suffix(".json"))

    with open(path) as file:
        # This ensures that comments in the XML files do not cause the
        # "no Alto namespace found" exception.
        parser = ET.XMLParser(remove_comments=True)
        tree = objectify.parse(file, parser=parser)
        root = RootAltoElement(
            tree.getroot(), alto_namespace=alto_namespace, dpi_x=dpi_x, dpi_y=dpi_y
        )

    # Skip empty files immediately
    if not len(root.content):
        logger.warning(f"No content found in file {path}")
        return

    # Parse styles and tags
    metadata_list = [
        AltoMetadata(
            target=target,
            metadata_list={
                node.attrib["ID"]: [
                    {
                        "name": key.capitalize(),
                        "value": value,
                        "type": "numeric" if value.isdigit() else "text",
                    }
                    for key, value in node.attrib.items()
                    if key != "ID"
                ]
                for node in root.content.findall(
                    f".//{{*}}{tag}/*", namespaces=root.namespaces
                )
                if node.attrib.get("ID")
            },
        )
        for tag, target in [("Styles", "STYLEREFS"), ("Tags", "TAGREFS")]
    ]

    page_nodes = root.content.findall(".//{*}Page", namespaces=root.namespaces)
    if len(page_nodes) == 1:
        # We use + here and not urljoin or path.join to create image URLs
        # because the base URL could contain a portion of the identifier:
        # 'http://server/iiif/root%2Fdirectory'
        # urljoin or path.join would erase that identifier prefix.
        if gallica:
            url = format_url(path, iiif_base_url, folders_ark_id_dict)
            image_id = create_iiif_image(client, url)
        else:
            iiif_path = (
                # Use the file identifier by default
                root.file_identifier
                # or keep existing path if we upload file of a subfolder
                or quote(str(path.parent / root.filename), safe="")
            )
            image_id = create_iiif_image(client, iiif_base_url + iiif_path)

        page_node = AltoElement(
            page_nodes[0],
            alto_namespace=alto_namespace,
            unit=root.unit,
            dpi_x=dpi_x,
            dpi_y=dpi_y,
        )
        page_node.parse_children()
        create_elements(
            client=client,
            nodes=[page_node],
            image_id=image_id,
            parent_id=parent_id,
            corpus_id=corpus["id"],
            worker_run_id=worker_run_id,
            cache=cache,
            publish_metadata=not skip_metadata,
            create_types=create_types,
            types_dict=types_dict,
            metadata_list=metadata_list,
        )
    elif len(page_nodes) > 1:
        for page_node in page_nodes:
            page_node = AltoElement(
                page_node,
                alto_namespace=alto_namespace,
                unit=root.unit,
                dpi_x=dpi_x,
                dpi_y=dpi_y,
            )
            if page_node.page_image_id is None:
                logger.warning(
                    "Attribute PHYSICAL_IMG_NR was not set for this Page node. Skipping…"
                )
                return
            image_id = create_iiif_image(
                client, iiif_base_url + page_node.page_image_id
            )

            create_elements(
                client=client,
                nodes=[page_node],
                image_id=image_id,
                parent_id=parent_id,
                corpus_id=corpus["id"],
                worker_run_id=worker_run_id,
                cache=cache,
                publish_metadata=not skip_metadata,
                create_types=create_types,
                types_dict=types_dict,
                metadata_list=metadata_list,
            )
    else:
        logger.warning(f"No Page node found in file {root.filename}. Skipping…")
        return


def run_gallica(
    metadata_file: Optional[Path] = None,
    *args,
    **kwargs,
):
    # If this is a Gallica import, load the metadata CSV file
    folders_ark_id_dict = dict()
    with open(metadata_file, "r") as file:
        reader = csv.reader(file)
        # Create a dictionary with the folder name as the id and the Gallica Ark ID as the value
        folders_ark_id_dict = {row[0]: row[1] for row in reader}

    run(
        folders_ark_id_dict=folders_ark_id_dict,
        gallica=True,
        *args,
        **kwargs,
    )


def run(
    path: Path,
    iiif_base_url: str,
    parent_id: UUID,
    worker_run_id: UUID,
    dpi_x: Optional[int] = None,
    dpi_y: Optional[int] = None,
    create_types: bool = False,
    existing_types: Optional[str] = None,
    folders_ark_id_dict: Optional[dict] = None,
    profile_slug: Optional[str] = None,
    gitlab_secure_file: Optional[Path] = None,
    gallica: bool = False,
    alto_namespace: Optional[str] = None,
    skip_metadata: bool = False,
) -> int:
    if (dpi_x is None) ^ (dpi_y is None):
        logger.error("--dpi-x and --dpi-y must be either both set or both unset.")
        return errno.EINVAL

    if dpi_x is not None and dpi_x <= 0:
        logger.error("--dpi-x must be a strictly positive integer.")
        return errno.EINVAL

    if dpi_y is not None and dpi_y <= 0:
        logger.error("--dpi-y must be a strictly positive integer.")
        return errno.EINVAL

    if not path.is_dir():
        logger.error(f"{path} is not a directory.")
        return errno.ENOTDIR

    file_paths = list(path.rglob("*.xml"))
    if not file_paths:
        logger.error(f"No XML files found in {path}.")
        return errno.ENOENT

    with Progress(transient=True) as progress:
        progress.add_task(start=False, description="Loading API client")
        client = Profiles(gitlab_secure_file).get_api_client_or_exit(profile_slug)

    with Progress(transient=True) as progress:
        progress.add_task(start=False, description="Fetching parent element")
        try:
            parent = client.request("RetrieveElement", id=parent_id)
        except ErrorResponse as e:
            logger.error(
                f"Could not retrieve parent element {parent_id}: HTTP {e.status_code} - {e.content}"
            )
            return errno.EREMOTEIO

    with Progress(transient=True) as progress:
        progress.add_task(start=False, description="Fetching corpus")
        corpus_id = parent["corpus"]["id"]
        try:
            corpus = client.request("RetrieveCorpus", id=corpus_id)
        except ErrorResponse as e:
            logger.error(
                f"Could not retrieve corpus {corpus_id}: HTTP {e.status_code} - {e.content}"
            )
            return errno.EREMOTEIO

    types_dict = None
    if existing_types:
        split_str = existing_types.split(" ")
        types_dict = {}
        for item in split_str:
            split_item = item.split(":")
            types_dict[str(split_item[0]).lower()] = str(split_item[1]).lower()
        for arkindex_type in types_dict.values():
            try:
                check_element_type(corpus, arkindex_type)
            except ValueError as e:
                logger.error(str(e))
                return errno.EINVAL

    failed = 0

    for file_path in track(file_paths, description="Uploading"):
        try:
            upload_alto_file(
                gallica=gallica,
                folders_ark_id_dict=folders_ark_id_dict,
                path=file_path,
                client=client,
                iiif_base_url=iiif_base_url,
                corpus=corpus,
                parent_id=parent_id,
                types_dict=types_dict,
                create_types=create_types,
                dpi_x=dpi_x,
                dpi_y=dpi_y,
                alto_namespace=alto_namespace,
                worker_run_id=worker_run_id,
                skip_metadata=skip_metadata,
            )
        except UploadProcessingError:
            logger.error(f"Failed to publish ALTO file @ {file_path}")
            failed += 1
    # Return a non-zero error code when all files have failed
    return failed >= len(file_paths)
