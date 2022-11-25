//
// Created by aichao on 2022/11/24.
//

#pragma

#include "src/utils/utils.h"
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

class FaceAPI {

public:
    FaceAPI(const std::string &model_dir,
            const std::vector<int> &functions,
            int device, int id);

    ~FaceAPI();


    ///人脸检测框
    SeetaFaceInfoArray Detect(const SeetaImageData &simage);

    ///人脸检测阈值
    void SetProperty(int property, float value);

    /// 人脸特征点检测5
    std::vector<SeetaPointF> mark5(const SeetaImageData &simage, const SeetaRect &box);

    /// 人脸特征点检测68
    std::vector<SeetaPointF> mark68(const SeetaImageData &simage, const SeetaRect &box);

    /// 设置活体阈值
    void SetLiveThreshold(float clarity, float reality);

    /// 活体检测
    int AliveDetect(const SeetaImageData &simage, const SeetaRect &box,
                    const std::vector<SeetaPointF> &points5);

    ///活体检测-返回清晰度跟活体值
    void GetAliveScore(float *clarity, float *reality);

    ///视频活体检测
    int VideoAliveDetect(const SeetaImageData &simage, const SeetaRect &box,
                         const std::vector<SeetaPointF> &points5);

    ///视频活体检测重置
    void ResetVideoAlive();

    ///五官遮挡检测
    std::vector<seeta::FaceLandmarker::PointWithMask>
    markMask(const SeetaImageData &simage, const SeetaRect &box);

    ///年龄检测
    int PredictAgeWithCrop(const SeetaImageData &simage,
                           const std::vector<SeetaPointF> &points5);

    /// 年龄检测使用裁剪好的图片（仅有人脸）
    int PredictAge(const SeetaImageData &simage);

    /// 性别检测
    int PredictGenderWithCrop(const SeetaImageData &simage,
                              const std::vector<SeetaPointF> &points5);

    /// 性别检测使用裁剪好的图片（仅有人脸）
    int PredictGender(const SeetaImageData &simage);

    ///口罩检测
    int DetectMask(const SeetaImageData &simage, const SeetaRect &box);

    ///人眼状态检测
    std::vector<int> DectectEye(const SeetaImageData &simage,
                                const std::vector<SeetaPointF> &points5);

    /// 清晰度评估
    int ClarityEvaluate(const SeetaImageData &simage,
                        const SeetaRect &box,
                        const std::vector<SeetaPointF> &points5);

    ///明亮度评估
    int BrightEvaluate(const SeetaImageData &simage,
                       const SeetaRect &box,
                       const std::vector<SeetaPointF> &points5);

    ///分辨率评估
    int ResolutionEvaluate(const SeetaImageData &simage,
                           const SeetaRect &box,
                           const std::vector<SeetaPointF> &points5);

    ///人脸姿态质量评估
    int PoseEvaluate(const SeetaImageData &simage,
                     const SeetaRect &box,
                     const std::vector<SeetaPointF> &points5);

    ///人脸完整性评估
    int IntegrityEvaluate(const SeetaImageData &simage,
                          const SeetaRect &box,
                          const std::vector<SeetaPointF> &points5);

    ///人脸跟踪
    SeetaTrackingFaceInfoArray Track(const SeetaImageData &simage);

    ///人脸跟踪清除
    void ResetTrack();

    ///人脸跟踪最小尺寸设置
    void SetTrackMinFaceSize(int facesize);

    ///人脸跟踪器的分辨率设置
    void SetTrackResolution(int width, int height);

    ///人脸跟踪人脸置信度设置
    void SetTrackThreshold(float threshold);

    ///人脸跟踪检测间隔
    void SetTrackInterval(int interval);

    ///人脸跟踪线程数设置
    void SetTrackThreads(int num);

    ///裁剪人脸
    SeetaImageData CropFace(const SeetaImageData &simage,
                            const std::vector<SeetaPointF> &points5);

    ///裁剪图特征提取
    std::vector<float> ExtractCroppedFace(const SeetaImageData &simage);

    ///原图提取特征
    std::vector<float> Extract(const SeetaImageData &simage,
                               const std::vector<SeetaPointF> &points5);

    ///相似度计算
    float CalculateSimilarity(const std::vector<float> &feature1,
                              const std::vector<float> &feature2);

private:
    ///
    void set_model_dir(const std::string &path);

    void set_device(int device, int id);

    void init_engine(const std::vector<int> &model_ids);

    /// 人脸检测器
    void initial_detector();

    /// 特征点5 检测器
    void initial_landmark5();

    /// 特征点68 检测器
    void initial_landmark68();

    /// 活体检测
    void initial_live();

    /// 五官遮挡检测
    void initial_facemask();

    /// 性别检测
    void initial_gender();

    /// 年龄检测
    void initial_age();

    /// 眼睛状态检测
    void initial_eyes();

    /// 口罩检测
    void initial_mask();

    /// 人脸跟踪
    void initial_tracking();

    /// 人脸识别
    void initial_recognition();

    /// 清晰度评估
    void initial_clarity();

    /// 两地评估
    void initial_bright();

    /// 分辨率评估
    void initial_resolution();

    /// 人脸姿态评估
    void initial_pose();

    /// 人脸完整性评估
    void initial_integrity();

private:
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
    std::string model_dir;
    SeetaDevice seetaDevice = SEETA_DEVICE_AUTO; //SEETA_DEVICE_AUTO = 0,SEETA_DEVICE_CPU  = 1,SEETA_DEVICE_GPU  = 2
    int deviceId = 0;                            //使用gpu 的id
    int track_width = 1920;                      //人脸跟踪视频的分辨率宽
    int track_height = 1080;                     //人脸跟踪视频的分辨率高
};
