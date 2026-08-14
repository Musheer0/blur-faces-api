# Blurfield

Blurfield is a privacy-focused video face-blurring platform. Upload a video or image and Blurfield automatically detects and blurs other people's faces to protect their privacy — while keeping your own face visible.

## How it works

1. Upload a video (or image) containing other people's faces.
2. Optionally upload a clear photo of your own face.
3. Blurfield automatically blurs everyone else's faces.
4. Download the privacy-safe video and share it without exposing bystanders' identities.

If you upload your face image, Blurfield uses it as the identity to preserve: your face stays visible while every other face in the video is blurred.

## Features

- **Auto face detection** — faces are detected frame-by-frame using a deep learning detector.
- **Selective blurring** — provide a reference image of your own face; everyone else is blurred, you stay visible.
- **Multiple blur methods** — choose between `pixelate`, `gaussian`, `blackout`, `elliptical`, and `median`.
- **Photo & video support** — blur faces in both images and videos.
- **Audio preserved** — for selective video blurring, the original audio is recovered and re-muxed into the output.
- **GPU accelerated** — runs on Modal with a CUDA-enabled image and FFmpeg encoding.

## Tech stack

- FastAPI + Modal (serverless ASGI app)
- uniface / ONNX Runtime for face detection, embeddings, and blurring
- OpenCV for frame processing
- FFmpeg for encoding and audio recovery
- boto3 / S3-compatible storage (e.g. Cloudflare R2)

## Project structure

```
src/
├── main.py              # Modal app entrypoint + FastAPI wiring
└── app/
    ├── api_middleware.py # API key auth
    ├── blur_video.py     # video face-blurring pipeline
    ├── blur_photo.py     # image face-blurring pipeline
    ├── detect_face.py    # face detection
    ├── recognizer.py     # face recognition (target identity)
    ├── anoymizer.py      # blur methods (pixelate, gaussian, blackout, ...)
    ├── s3.py             # S3 upload/download helpers
    └── routes/
        ├── video_routes.py  # /api/blur-video endpoints
        └── photo_routes.py  # /api/blur-photo endpoints
```

## Configuration

Copy these into your environment (`.env` file or Modal secret named `face-blur`):

```env
S3_BUCKET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_ENDPOINT_URL_S3=
AWS_ENDPOINT_URL_IAM=
AWS_REGION=auto
API_KEY=
```

- `S3_BUCKET` — bucket used for storing input and output media.
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` — credentials for S3-compatible storage.
- `AWS_ENDPOINT_URL_S3` — S3 endpoint URL (e.g. Cloudflare R2).
- `AWS_ENDPOINT_URL_IAM` — IAM endpoint URL.
- `AWS_REGION` — region (defaults to `auto`).
- `API_KEY` — secret key required in the `X-API-Key` header for all API requests.

## API

All requests require the header `X-API-Key: <API_KEY>`.

### Blur a video

`POST /api/blur-video`

```json
{
  "key": "input/video.mp4",
  "output_key": "output/video-blurred.mp4",
  "blur_method": "pixelate"
}
```

### Blur a video selectively (keep your face)

`POST /api/blur-video/selective`

```json
{
  "key": "input/video.mp4",
  "output_key": "output/video-blurred.mp4",
  "blur_method": "gaussian",
  "target_image": "input/my-face.jpg"
}
```

### Blur a photo

`POST /api/blur-photo`

```json
{
  "key": "input/photo.jpg",
  "output_key": "output/photo-blurred.jpg",
  "blur_method": "blackout"
}
```

### Blur a photo selectively

`POST /api/blur-photo/selective`

```json
{
  "key": "input/photo.jpg",
  "output_key": "output/photo-blurred.jpg",
  "blur_method": "gaussian",
  "target_image": "input/my-face.jpg"
}
```

### Health check

`GET /health`

### Blur methods

| Value        | Description            |
| ------------ | ---------------------- |
| `pixelate`   | Pixelated face blocks  |
| `gaussian`   | Gaussian blur          |
| `blackout`   | Solid black overlay    |
| `elliptical` | Elliptical-shaped blur |
| `median`     | Median filter blur     |

## Deployment

The app is deployed as a Modal serverless app:

```bash
modal deploy src/main.py
```

The Modal secret `face-blur` must contain the environment variables listed above.
