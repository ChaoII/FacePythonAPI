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
#include <seeta/MaskDetector.h>        //口罩检测
#include <seeta/EyeStateDetector.h>    //眼睛状态检测
#include <seeta/AgePredictor.h>        //年龄检测
#include <seeta/GenderPredictor.h>     //性别检测
#include <seeta/QualityStructure.h>    //遮挡评估
#include <seeta/QualityOfBrightness.h> //亮度评估
#include <seeta/QualityOfResolution.h> //分辨率评估
#include <seeta/QualityOfIntegrity.h>  //完整性评估
#include <seeta/QualityOfClarity.h>    //清晰度检测(传统)
#include <seeta/QualityOfPose.h>       //姿态评估(传统)
#include <seeta/FaceRecognizer.h>      //人脸识别
#include <seeta/FaceTracker.h>         //人脸跟踪


#if defined(_WIN32)
#ifdef FACE_LIB
#define FACEAPI __declspec(dllexport)
#else
#define FACEAPI __declspec(dllimport)
#endif  // FACE_LIB
#else
#define FACEAPI __attribute__((visibility("default")))
#endif  // _WIN32
#ifdef __cplusplus
extern "C" {
#endif
seeta::FaceDetector *faceDetector = nullptr;           //人脸框
seeta::FaceLandmarker *landDetector5 = nullptr;        //5特征点
seeta::FaceLandmarker *landDetector68 = nullptr;       //68特征点
seeta::FaceAntiSpoofing *liveDetector = nullptr;       //活体检测
seeta::FaceLandmarker *faceMaskDetector = nullptr;     //五官遮挡检测
seeta::AgePredictor *agePredictor = nullptr;           //年龄预测
seeta::GenderPredictor *genderPredictor = nullptr;     //性别评估
seeta::MaskDetector *maskDetector = nullptr;           //口罩检测
seeta::EyeStateDetector *eyeStateDetector = nullptr;   //眼睛状态检测
seeta::QualityRule *qualityClarity = nullptr;          //清晰度评估(传统)
seeta::QualityRule *qualityBright = nullptr;           //明亮度评估(传统)
seeta::QualityRule *qualityResolution = nullptr;       //分辨率评估
seeta::QualityOfPose *qualityPose = nullptr;           //姿态评估(传统)
seeta::QualityOfIntegrity *qualityIntegrity = nullptr; //完整性评估
seeta::FaceRecognizer *faceRecognizer = nullptr;       //人脸识别faceFecognition
seeta::FaceTracker *faceTracker = nullptr;             //人脸跟踪器
static std::string model_path = "";
static SeetaDevice seetaDevice = SEETA_DEVICE_AUTO; //SEETA_DEVICE_AUTO = 0,SEETA_DEVICE_CPU  = 1,SEETA_DEVICE_GPU  = 2
static int deviceId = 0;                            //使用gpu 的id
static int track_width = 1920;                      //人脸跟踪视频的分辨率宽
static int track_height = 1080;                     //人脸跟踪视频的分辨率高


FACEAPI void get_model_path(const char *path);
FACEAPI void set_device(int device, int id);
FACEAPI int InitEngine(const int *model_ids, int len);
FACEAPI int UnloadEngine();
///人脸检测框
FACEAPI SeetaFaceInfoArray Detect(const SeetaImageData &simage);
///人脸检测阈值
FACEAPI void SetProperty(int property, float value);
/// 人脸特征点检测5
FACEAPI int mark5(const SeetaImageData &simage, const SeetaRect &box, SeetaPointF points5[5]);
/// 人脸特征点检测68
FACEAPI int mark68(const SeetaImageData &simage, const SeetaRect &box, SeetaPointF points68[68]);
/// 设置活体阈值
FACEAPI void SetLiveThreshold(float clarity, float reality);
/// 活体检测
FACEAPI int Predict(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);
///活体检测-返回清晰度跟活体值
FACEAPI void GetPreFrameScore(float *clarity, float *reality);
///视频活体检测
FACEAPI int PredictVideo(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);
///视频活体检测重置
FACEAPI void ResetVideo();
///五官遮挡检测
FACEAPI int markMask(const SeetaImageData &simage, const SeetaRect &box, SeetaPointF points5[5], int face_mask[5]);
///年龄检测
FACEAPI int PredictAgeWithCrop(const SeetaImageData &simage, const SeetaPointF points5[5]);
/// 年龄检测使用裁剪好的图片（仅有人脸）
FACEAPI int PredictAge(const SeetaImageData &simage);
/// 性别检测
FACEAPI int PredictGenderWithCrop(const SeetaImageData &simage, const SeetaPointF points5[5]);
/// 性别检测使用裁剪好的图片（仅有人脸）
FACEAPI int PredictGender(const SeetaImageData &simage);
///口罩检测
FACEAPI int DetectMask(const SeetaImageData &simage, const SeetaRect &box);
///人眼状态检测
FACEAPI void DectectEye(const SeetaImageData &simage, const SeetaPointF points5[5], int states[2]);
/// 清晰度评估
FACEAPI int ClarityEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);
///明亮度评估
FACEAPI int BrightEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);
///分辨率评估
FACEAPI int ResolutionEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);
///人脸姿态质量评估
FACEAPI int PoseEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);
///人脸完整性评估
FACEAPI int IntegrityEvaluate(const SeetaImageData &simage, const SeetaRect &box, const SeetaPointF points5[5]);
///人脸跟踪
FACEAPI SeetaTrackingFaceInfoArray Track(const SeetaImageData &simage);
///人脸跟踪清除
FACEAPI void Reset();
///人脸跟踪最小尺寸设置
FACEAPI void SetMinFaceSize(int facesize);
///人脸跟踪器的分辨率设置
FACEAPI void SetTrackResolution(int width, int height);
///人脸跟踪人脸置信度设置
FACEAPI void SetThreshold(float threshold);
///人脸跟踪检测间隔
FACEAPI void SetInterval(int interval);
//人脸跟踪线程数设置
FACEAPI void SetSingleCalculationThreads(int num);
//裁剪人脸
FACEAPI SeetaImageData CropFace(const SeetaImageData &simage, const SeetaPointF points5[5]);
//裁剪图特征提取
FACEAPI int ExtractCroppedFace(const SeetaImageData &simage, float feature[1024]);
//原图提取特征
FACEAPI int Extract(const SeetaImageData &simage, const SeetaPointF points5[5], float feature[1024]);
//相似度计算
FACEAPI float CalculateSimilarity(const float feature1[1024], const float feature2[1024]);
#ifdef __cplusplus
}
#endif