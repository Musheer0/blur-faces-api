import logging
import os

from fastapi import APIRouter, Depends, HTTPException

from app.api_middleware import apiMiddleware
from app.blur_video import blur_video, blur_video_by_target
from app.modals import BlurVideoRequest, BlurVideoRequestSelective

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/blur-video",
    dependencies=[Depends(apiMiddleware)],
)


def _recovered_path(path: str) -> str:
    root, ext = os.path.splitext(path)
    return f"{root}_recovered{ext}"


def _cleanup(*paths: str) -> None:
    for path in paths:
        try:
            os.remove(path)
        except OSError as e:
            logger.warning("Failed to delete file %s: %s", path, e)


@router.post("")
def blur_video_api(body: BlurVideoRequest):
    from app.s3 import download_video, upload_video

    try:
        file_path = download_video(body.key)
        logger.info("Downloaded video: %s", file_path)
        output = blur_video(
            method=body.blur_method,
            input=file_path,
            output=body.output_key,
        )
        upload_video(body.output_key, output)
        return {"success": True, "key": body.output_key}
    except Exception as e:
        logger.exception("Failed to blur video: %s", e)
        raise HTTPException(status_code=400, detail="Error processing video try again")


@router.post("/selective")
def blur_video_selective_api(body: BlurVideoRequestSelective):
    from app.s3 import download_video, upload_video
    from app.recover_audio import recover_audio

    logger.debug("Request body: %s", body)
    try:
        file_path = download_video(body.key)
        target_file_path = download_video(body.target_image)
        output = blur_video_by_target(
            method=body.blur_method,
            input=file_path,
            output=body.output_key,
            target_img=target_file_path,
        )
        recovered_video = recover_audio(
            input=output,
            output=_recovered_path(output),
            audio_video=file_path,
        )
        upload_video(body.output_key, recovered_video)
        _cleanup(file_path, target_file_path, recovered_video, output)
        return {"success": True, "key": body.output_key}
    except Exception as e:
        logger.exception("Failed to blur video by target: %s", e)
        raise HTTPException(status_code=400, detail="Error processing video try again")
