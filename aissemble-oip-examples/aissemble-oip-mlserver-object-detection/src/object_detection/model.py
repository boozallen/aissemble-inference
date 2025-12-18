import base64
import io
from PIL import Image
from mlserver import MLModel
from mlserver.codecs import StringCodec
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput
from transformers import pipeline

class ImgDetection(MLModel):

    async def load(self) -> bool:
        pipe = pipeline("object-detection", model="hustvl/yolos-small")
        self.model = pipe
        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """
        Perform object detection on a base64-encoded image.

        Args:
            payload: InferenceRequest containing a base64-encoded image string in the first input

        Returns:
            InferenceResponse with three outputs:
                - labels: Detected object class names
                - scores: Confidence scores for each detection
                - boxes: Bounding box coordinates [xmin, ymin, xmax, ymax] for each detection
        """
        # decode base64-encoded img string from request, grab first element from first RequestInput list
        input_data = StringCodec.decode_input(payload.inputs[0])[0]

        # convert to PIL image
        image_bytes = base64.b64decode(input_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # run object detection with loaded YOLO model
        results = self.model(image)

        print(f'results type: {type(results)}')
        
        # get results and put them into separate lists
        labels = [item['label'] for item in results]
        scores = [item['score'] for item in results]
        boxes = [list(item['box'].values()) for item in results]  # [xmin, ymin, xmax, ymax]
        
        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[
                ResponseOutput(
                    name="labels",
                    shape=[len(labels)],
                    datatype="BYTES",
                    data=labels,
                ),
                ResponseOutput(
                    name="scores",
                    shape=[len(scores)],
                    datatype="FP32",
                    data=scores,
                ),
                ResponseOutput(
                    name="boxes",
                    shape=[len(boxes), 4], # reshape into length boxes with 4 coordinates each
                    datatype="FP32",
                    data=[coord for box in boxes for coord in box], # flatten boxes bc ResponseOutput.data expects 1D list
                ),
            ],
        )