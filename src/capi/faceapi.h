//
// Created by aichao on 2022/11/15.
//
#pragma once

#include "src/utils/utils.h"
#include <iostream>
#include <seeta/Common/Struct.h>
#include <seeta/FaceDetector.h>
#include <seeta/FaceLandmarker.h>
#include <seeta/FaceAntiSpoofing.h>
#include <seeta/MaskDetector.h>
#include <seeta/EyeStateDetector.h>
#include <seeta/AgePredictor.h>
#include <seeta/GenderPredictor.h>
#include <seeta/QualityStructure.h>
#include <seeta/QualityOfBrightness.h>
#include <seeta/QualityOfResolution.h>
#include <seeta/QualityOfIntegrity.h>
#include <seeta/QualityOfClarity.h>
#include <seeta/QualityOfPose.h>
#include <seeta/FaceRecognizer.h>
#include <seeta/FaceTracker.h>

#ifdef __cplusplus
extern "C" {
#endif

seeta::FaceDetector *faceDetector = nullptr;

seeta::FaceLandmarker *landDetector5 = nullptr;

seeta::FaceLandmarker *landDetector68 = nullptr;

seeta::FaceAntiSpoofing *liveDetector = nullptr;

seeta::FaceLandmarker *faceMaskDetector = nullptr;

seeta::AgePredictor *agePredictor = nullptr;

seeta::GenderPredictor *genderPredictor = nullptr;

seeta::MaskDetector *maskDetector = nullptr;

seeta::EyeStateDetector *eyeStateDetector = nullptr;

seeta::QualityRule *qualityClarity = nullptr;

seeta::QualityRule *qualityBright = nullptr;

seeta::QualityRule *qualityResolution = nullptr;

seeta::QualityOfPose *qualityPose = nullptr;

seeta::QualityOfIntegrity *qualityIntegrity = nullptr;

seeta::FaceRecognizer *faceRecognizer = nullptr;

seeta::FaceTracker *faceTracker = nullptr;
static std::string model_path = "";
static SeetaDevice seetaDevice = SEETA_DEVICE_AUTO; //SEETA_DEVICE_AUTO = 0,SEETA_DEVICE_CPU  = 1,SEETA_DEVICE_GPU  = 2

static int deviceId = 0;

static int track_width = 1920;

static int track_height = 1080;


FACEAPI void get_model_path(const char *path);
FACEAPI void set_device(int device, int id);
FACEAPI int InitEngine(const int *model_ids, int len);
FACEAPI int UnloadEngine();

FACEAPI SeetaFaceInfoArray Detect(const SeetaImageData &simage);

FACEAPI void SetProperty(int property, float value);

FACEAPI int mark5(const SeetaImageData &simage, const SeetaRect &box, SeetaPointF points5[5]);

FACEAPI int mark68(const SeetaImageData &simage, const SeetaRect &box, SeetaPointF points68[68]);

FACEAPI void SetLiveThreshold(float clarity, float reality);

FACEAPI int Predict(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);

FACEAPI void GetPreFrameScore(float *clarity, float *reality);

FACEAPI int PredictVideo(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);

FACEAPI void ResetVideo();

FACEAPI int markMask(const SeetaImageData &simage, const SeetaRect &box, SeetaPointF points5[5], int face_mask[5]);

FACEAPI int PredictAgeWithCrop(const SeetaImageData &simage, const SeetaPointF points5[5]);

FACEAPI int PredictAge(const SeetaImageData &simage);

FACEAPI int PredictGenderWithCrop(const SeetaImageData &simage, const SeetaPointF points5[5]);

FACEAPI int PredictGender(const SeetaImageData &simage);

FACEAPI int DetectMask(const SeetaImageData &simage, const SeetaRect &box);

FACEAPI void DectectEye(const SeetaImageData &simage, const SeetaPointF points5[5], int states[2]);

FACEAPI int ClarityEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);

FACEAPI int BrightEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);

FACEAPI int ResolutionEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);

FACEAPI int PoseEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);

FACEAPI int IntegrityEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);

FACEAPI SeetaTrackingFaceInfoArray Track(const SeetaImageData &simage);

FACEAPI void Reset();

FACEAPI void SetMinFaceSize(int facesize);

FACEAPI void SetTrackResolution(int width, int height);

FACEAPI void SetThreshold(float threshold);

FACEAPI void SetInterval(int interval);

FACEAPI void SetSingleCalculationThreads(int num);

FACEAPI SeetaImageData
CropFace(const SeetaImageData &simage, const SeetaPointF points5[5]);

FACEAPI int ExtractCroppedFace(const SeetaImageData &simage, float feature[1024]);

FACEAPI int Extract(const SeetaImageData &simage, const SeetaPointF points5[5], float feature[1024]);

FACEAPI float CalculateSimilarity(const float feature1[1024], const float feature2[1024]);
#ifdef __cplusplus
}
#endif