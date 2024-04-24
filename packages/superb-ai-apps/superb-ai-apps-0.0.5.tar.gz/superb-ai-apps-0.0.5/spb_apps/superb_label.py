import logging
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

import phy_credit
import requests
from PIL import Image
from spb_label import sdk as spb_label
from spb_label.exceptions import ParameterException
from spb_label.utils import SearchFilter

from spb_apps.apps import SuperbApps
from spb_apps.utils.converter import convert_yolo_bbox
from spb_apps.utils.utils import call_with_retry

logger = logging.getLogger("superb_label")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

formatter_debug = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
handler_debug = logging.FileHandler("log_event.log")
handler_debug.setLevel(logging.DEBUG)
handler_debug.setFormatter(formatter_debug)

logger.addHandler(handler)
logger.addHandler(handler_debug)


class SuperbLabel(SuperbApps):
    def __init__(
        self,
        team_name: str,
        access_key: str,
        project_id: str = "",
        project_name: str = "",
    ):
        """
        Initializes the SuperbLabel class with necessary details for operation.

        Parameters:
        - team_name (str): The name of the team.
        - access_key (str): The access key for authentication.
        - project_id (str, optional): The ID of the project to be set for the client. Defaults to an empty string.
        - project_name (str, optional): The name of the project. Defaults to an empty string.
        """
        self.team_name: str = team_name
        self.access_key: str = access_key
        super().__init__(team_name, access_key)
        self.client = spb_label.Client(
            team_name=team_name,
            access_key=access_key,
            project_id=project_id if project_id else None,
            project_name=project_name if project_name else None,
        )

    def change_project(self, project_name: str):
        """
        Changes the project context for the label client.

        Parameters:
            project_name (str): The name of the project to switch to.
        """
        self.client.set_project(name=project_name)

    def get_label_interface(self) -> Dict:
        """
        Retrieves the label interface configuration for the 'label' platform.

        Returns:
            Dict: The label interface configuration.
        """
        lb_interface = self.client.project.label_interface
        return lb_interface

    def download_image_by_filter(
        self,
        tags: list = [],
        data_key: str = "",
        status: list = [],
        path: str = None,
    ):
        """
        Downloads images by applying filters such as tags, data key, and status.

        Parameters:
            tags (list, optional): A list of tags to filter images. Defaults to [].
            data_key (str, optional): A specific data key to filter images. Defaults to "".
            status (list, optional): A list of statuses to filter images. Defaults to [].
            path (str, optional): The local file path to save the downloaded images. Defaults to None.
        """
        from concurrent.futures import ThreadPoolExecutor

        def download(label):
            self.download_image(label=label, path=path)

        count, labels = self.client.get_labels(
            tags=tags, data_key=data_key, status=status
        )
        print(f"Downloading {count} data to {path}")
        if count > 50:
            with ThreadPoolExecutor(max_workers=4) as executor:
                executor.map(download, labels)
        else:
            for label in labels:
                download(label)

    def download_export(
        self,
        input_path: str,
        export_id: str,
    ):
        """
        Download an export from the server to a local path.

        Parameters:
        - input_path (str): The local file path where the export will be saved.
        - export_id (str): The ID of the export to download.
        """
        print("[INFO] Checking for the export to be downloaded...")
        download_url = self.client.get_export(id=export_id).download_url
        r = requests.get(download_url)
        if r.status_code == 200:
            print("Saving export to local path")
            Path(input_path).parents[0].mkdir(parents=True, exist_ok=True)
            with open(input_path, "wb") as f:
                f.write(r.content)
        else:
            print(f"Failed to download the file. Status code: {r.status_code}")

    def get_labels(
        self,
        data_key: str = None,
        tags: list = None,
        assignees: list = None,
        status: list = None,
        all: bool = False,
    ) -> Tuple[int, List]:
        """
        Retrieve labels based on provided filters or all labels if specified.

        Parameters:
        - data_key (str, optional): Filter for a specific data key. Defaults to an empty string.
        - tags (list, optional): Filter for specific tags. Defaults to an empty list.
        - assignees (list, optional): Filter for specific assignees. Defaults to an empty list.
        - status (list, optional): Filter for specific status. Defaults to an empty list.
        - all (bool, optional): If True, ignores other filters and retrieves all labels. Defaults to False.

        Returns:
        Tuple[int, List]: A tuple containing the count of labels and a list of labels.
        """
        if all:
            # [ ] BUG: all 일때 커서가 다음으로 넘어가지 않음
            next_cursor = None
            count, labels, next_cursor = call_with_retry(
                fn=self.client.get_labels, cursor=next_cursor
            )

        else:
            filter = SearchFilter(project=self.client.project)
            if data_key:
                filter.data_key_matches = data_key
            if tags:
                filter.tag_name_all = tags
            if assignees:
                filter.assignee_is_any_one_of = assignees
            if status:
                filter.status_is_any_one_of = status
            next_cursor = None
            count, labels, next_cursor = call_with_retry(
                fn=self.client.get_labels, filter=filter, cursor=next_cursor
            )

            # [x] TODO: 검색된 라벨이 없을 때의 예외처리
            if count == 0:
                labels = None
                return count, labels

        return count, labels

    def download_image(
        self,
        label: spb_label.DataHandle = None,
        data_key: str = None,
        path: str = "",
    ):
        """
        Download an image associated with a label to a specified path.

        Parameters:
        - label (spb_label.DataHandle, optional): The label data handle containing the image to download. If None, the label is retrieved using the data_key.
        - data_key (str, optional): The unique identifier for the image. Used if label is None.
        - path (str): The local file path where the image will be saved. Defaults to "/".
        """
        if label is None:
            label = self.client.get_label(data_key=data_key)
        label.download_image(download_to=path)

    def get_width_height(
        self, label: spb_label.DataHandle = None, data_key: str = None
    ) -> Tuple[int, int]:
        """
        Download an image associated with a label, return its width and height, and delete the image.

        Parameters:
        - label (spb_label.DataHandle, optional): The label data handle containing the image to download. If None, the label is retrieved using the data_key.
        - data_key (str, optional): The unique identifier for the image. Used if label is None.

        Returns:
        Tuple[int, int]: A tuple containing the width and height of the downloaded image.
        """
        if label is None:
            label = self.client.get_label(data_key=data_key)
        image_url = label.get_image_url()
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        width, height = img.size

        return width, height

    def make_bbox_annotation(self, class_name: str, annotation: list):
        """
        Create a bounding box setting for a given class name and annotation coordinates.

        Parameters:
        - class_name (str): The class name associated with the bounding box.
        - annotation (list): A list containing the coordinates of the bounding box in the order [x, y, width, height].

        Returns:
        A tuple containing the class name and a dictionary with the bounding box coordinates.
        """
        bbox = {
            "class_name": class_name,
            "annotation": {
                "coord": {
                    "x": annotation[0],
                    "y": annotation[1],
                    "width": annotation[2],
                    "height": annotation[3],
                }
            },
        }

        return bbox

    def convert_yolo_bbox_to_platform(
        self,
        data_key: str,
        annotations: list,
        classes: list,
    ) -> Tuple[Optional[str], Optional[list]]:
        """
        Convert YOLO bounding box annotations to the format expected by the platform.

        Returns:
            Tuple[Optional[str], Optional[list]]: A tuple containing the data handler and the converted annotations if successful, otherwise None for each.
        """
        _, label = self.client.get_labels(data_key=data_key)
        if len(label) == 0:
            print(
                f"[SKIPPED] Data key: {data_key}, does not exist in project {self.client.get_project_name()}"
            )
            return None, None
        data_handler = label[0]
        if classes == "":
            print("To upload yolo annotations, you must provide classes.")
            return None, None
        width, height = self.get_width_height(data_handler=data_handler)
        converted_annotations = convert_yolo_bbox(
            data_key, annotations, classes, width, height
        )
        label_annotations = []
        for anno in converted_annotations:
            bbox = self.make_bbox_annotation(anno[0], anno[1])
            label_annotations.append(bbox)

        return data_handler, label_annotations

    def upload_images(self, image_paths: list, dataset_name: str):
        """
        Upload images to a specified dataset.

        Parameters:
        - image_paths (list): A list of paths to the images to be uploaded.
        - dataset_name (str): The name of the dataset to upload the images to.
        """
        for path in image_paths:
            try:
                self.client.upload_image(path, dataset_name)
            except ParameterException as e:
                print(f"[ERROR]: Uploading went wrong: {e}")

    def upload_annotation(
        self,
        label: spb_label.DataHandle,
        annotations: list,
        overwrite: bool = False,
    ):
        """
        Upload annotations for a given label.

        Parameters:
        - label (spb_label.DataHandle): The label to which the annotations will be added.
        - annotations (list): A list of annotations to be added to the label.
        - overwrite (bool, optional): A flag indicating whether existing annotations should be overwritten. Defaults to False.
        """
        if overwrite:
            labels = []
            for anno in annotations:
                try:
                    bbox = self.make_bbox_annotation(
                        class_name=anno[0], annotation=anno[1]
                    )
                except Exception:
                    raise Exception(
                        f"[ERROR]: Error occurred while making bbox, check the annotation format || {anno}"
                    )
                labels.append(bbox)
            if len(labels) == 0:
                raise Exception(f"[ERROR]: No annotations found for the label")
            call_with_retry(fn=label.set_object_labels, labels=labels)
        else:
            for anno in annotations:
                try:
                    bbox = self.make_bbox_annotation(
                        class_name=anno[0], annotation=anno[1]
                    )
                except Exception:
                    raise Exception(
                        f"[ERROR]: Error occurred while making bbox, check the annotation format || {anno}"
                    )
                if "class_name" not in bbox or "annotation" not in bbox:
                    raise Exception(
                        "[ERROR]: No annotations found for the label"
                    )
                call_with_retry(
                    fn=label.add_object_label,
                    class_name=bbox["class_name"],
                    annotation=bbox["annotation"],
                )
        call_with_retry(fn=label.update_info)

    def build_label_interface(
        self,
        format: str,
        class_list: list,
        bbox: bool,
    ):
        """
        Build and update the label interface for the project based on the provided class list and bounding box flag.

        Parameters:
        - class_list (list): A list of class names to be included in the label interface.
        - bbox (bool): A flag indicating whether bounding boxes should be used.

        Returns:
        A tuple containing the updated label interface and a category map.
        """

        if format.lower() == "yolo":
            existing_label_interface = self.client.project.label_interface
            if existing_label_interface:
                label_interface = phy_credit.imageV2.LabelInterface.from_dict(
                    existing_label_interface
                )
                object_detection = (
                    phy_credit.imageV2.ObjectDetectionDef.from_dict(
                        existing_label_interface.get("object_detection")
                    )
                )
            else:
                label_interface = (
                    phy_credit.imageV2.LabelInterface.get_default()
                )
                object_detection = (
                    phy_credit.imageV2.ObjectDetectionDef.get_default()
                )

            category_map = dict()
            for class_name in class_list:
                bbox_suite_class_id = str(uuid4())
                bbox_suite_class_name = class_name

                object_detection.add_box(
                    name=bbox_suite_class_name, id=bbox_suite_class_id
                )

            label_interface.set_object_detection(
                object_detection=object_detection
            )

            self.client.update_project(
                id=self.client.project.id,
                label_interface=label_interface.to_dict(),
            )
        return label_interface, category_map
