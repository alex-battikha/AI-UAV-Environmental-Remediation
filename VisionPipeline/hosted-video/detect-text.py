from roboflow import Roboflow

rf = Roboflow(api_key="aH5jTaXPJvyiHjfTnbHC")
project = rf.workspace().project("uav-pollutant-detection-v3-mxokp")
model = project.version("1").model

job_id, signed_url, expire_time = model.predict_video(
    "validation-videos/comp_test.mp4",
    fps=5,
    prediction_type="batch-video",
)

results = model.poll_until_video_results(job_id)

print(results)

