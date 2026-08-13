import logging
import os

from fastapi import APIRouter, Depends, HTTPException

from app.api_middleware import apiMiddleware
from app.blur_photo import blur_photo, blur_photo_by_target
from app.modals import BlurPhotoRequest, BlurPhotoRequestSelective

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/blur-photo",
    dependencies=[Depends(apiMiddleware)],
)


def _cleanup(*paths: str) -> None:
    for path in paths:
        try:
            os.remove(path)
        except OSError as e:
            logger.warning("Failed to delete file %s: %s", path, e)


@router.post("")
def blur_photo_api(body: BlurPhotoRequest):
    from app.s3 import download_image, upload_image

    try:
        file_path = download_image(body.key)
        output = blur_photo(
            method=body.blur_method,
            input=file_path,
            output=body.output_key,
        )
        upload_image(body.output_key, output)
        return {"success": True, "key": body.output_key}
    except Exception as e:
        logger.exception("Failed to blur photo: %s", e)
        raise HTTPException(status_code=400, detail="Error processing image try again")


@router.post("/selective")
def blur_photo_selective_api(body: BlurPhotoRequestSelective):
    from app.s3 import download_image, upload_image

    try:
        file_path = download_image(body.key)
        target_file_path = download_image(body.target_image)

        output = blur_photo_by_target(
            method=body.blur_method,
            input=file_path,
            output=body.output_key,
            target_img=target_file_path,
        )

        upload_image(body.output_key, output)

        _cleanup(file_path, target_file_path, output)

        return {"success": True, "key": body.output_key}
    except Exception as e:
        logger.exception("Failed to blur photo by target: %s", e)
        raise HTTPException(status_code=400, detail="Error processing image try again")
