//
// Created by aichao on 2022/11/24.
//

#include <iostream>
#include "src/pybind/FaceAPI.h"

using namespace std;

FaceAPI::FaceAPI(const std::string &model_dir,
                 const std::vector<int> &functions,
                 int device, int id) {

    set_model_dir(model_dir);

    set_device(device, id);

    init_engine(functions);
}

void FaceAPI::initial_detector() {
    seeta::ModelSetting setting;
    setting.device = seetaDevice; //GPU CPU AUTO
    setting.id = deviceId;
    setting.append(model_dir + "/face_detector.csta");
    //按调用文件所在的工作目录文件所在的路径为参考,而不是动态库所在路径.但如果是执行文件,那么按执行文件的位置
    faceDetector = new seeta::FaceDetector(setting);
}

// 特征点5 检测器
void FaceAPI::initial_landmark5() {
    seeta::ModelSetting setting;
    setting.device = seetaDevice; //GPU CPU AUTO
    setting.id = deviceId;
    setting.append(model_dir + "/face_landmarker_pts5.csta");
    landDetector5 = new seeta::FaceLandmarker(setting);
}

// 特征点68 检测器
void FaceAPI::initial_landmark68() {
    seeta::ModelSetting setting;
    setting.device = seetaDevice; //GPU CPU AUTO
    setting.id = deviceId;
    setting.append(model_dir + "/face_landmarker_pts68.csta");
    landDetector68 = new seeta::FaceLandmarker(setting);
}

/// 活体检测
void FaceAPI::initial_live() {
    seeta::ModelSetting setting;
    setting.device = seetaDevice; //GPU CPU AUTO
    setting.id = deviceId;
    setting.append(model_dir + "/fas_first.csta");
    setting.append(model_dir + "/fas_second.csta");
    liveDetector = new seeta::FaceAntiSpoofing(setting);
}

///五官遮挡检测
void FaceAPI::initial_facemask() {
    seeta::ModelSetting setting;
    setting.device = seetaDevice; //GPU CPU AUTO
    setting.id = deviceId;
    setting.append(model_dir + "/face_landmarker_mask_pts5.csta");
    faceMaskDetector = new seeta::FaceLandmarker(setting);
}

////性别检测
void FaceAPI::initial_gender() {
    seeta::ModelSetting setting;
    setting.device = seetaDevice; //GPU CPU AUTO
    setting.id = deviceId;
    setting.append(model_dir + "/gender_predictor.csta");
    genderPredictor = new seeta::GenderPredictor(setting);
}

////年龄检测
void FaceAPI::initial_age() {
    seeta::ModelSetting setting;
    setting.device = seetaDevice; //GPU CPU AUTO
    setting.id = deviceId;
    setting.append(model_dir + "/age_predictor.csta");
    agePredictor = new seeta::AgePredictor(setting);
}

///眼睛状态检测
void FaceAPI::initial_eyes() {
    seeta::ModelSetting setting;
    setting.device = seetaDevice; //GPU CPU AUTO
    setting.id = deviceId;
    setting.append(model_dir + "/eye_state.csta");
    eyeStateDetector = new seeta::EyeStateDetector(setting);
}

////口罩检测
void FaceAPI::initial_mask() {
    seeta::ModelSetting setting;
    setting.device = seetaDevice; //GPU CPU AUTO
    setting.id = deviceId;
    setting.append(model_dir + "/mask_detector.csta");
    maskDetector = new seeta::MaskDetector(setting);
}

///人脸跟踪
void FaceAPI::initial_tracking() {
    seeta::ModelSetting setting;
    setting.append(model_dir + "/face_detector.csta");
    faceTracker = new seeta::FaceTracker(setting, track_width, track_height);
}

/// 人脸识别
void FaceAPI::initial_recognition() {
    seeta::ModelSetting setting;
    setting.append(model_dir + "/face_recognizer.csta");
    faceRecognizer = new seeta::FaceRecognizer(setting);
}

/// 清晰度评估(传统)
void FaceAPI::initial_clarity() {
    qualityClarity = new seeta::QualityOfClarity();
}

/// 明亮度评估(传统)
void FaceAPI::initial_bright() {
    qualityBright = new seeta::QualityOfBrightness();
}

/// 分辨率评估(传统)
void FaceAPI::initial_resolution() {
    qualityResolution = new seeta::QualityOfResolution();
}

/// 姿态评估(传统)
void FaceAPI::initial_pose() {
    qualityPose = new seeta::QualityOfPose();
}

/// 人脸完整性评估
void FaceAPI::initial_integrity() {
    qualityIntegrity = new seeta::QualityOfIntegrity();
}


/// 设置模型文件目录
void FaceAPI::set_model_dir(const std::string &dir) {
    FRINFO << "model dir:" << dir << endl;
    model_dir = dir;
}

///设置使用gpu还是cpu还是auto,默认为auto
void FaceAPI::set_device(int device, int id) {
    if (device == 0) {
        seetaDevice = SEETA_DEVICE_AUTO;
        FRINFO << "FaceApi device : AUTO" << endl;
    } else if (device == 1) {
        seetaDevice = SEETA_DEVICE_CPU;
        FRINFO << "FaceApi device : CPU" << endl;
    } else if (device == 2) {
        seetaDevice = SEETA_DEVICE_GPU;
        FRINFO << "FaceApi device : GPU" << endl;
    } else {
        FRERROR << "unsupported device, only supported in [0:auto, 1:cpu, 2:gpu]" << std::endl;
    }
    deviceId = id;
    FRINFO << "deviceId=" << deviceId << endl;
}

//加载模型 , 求的数组长度错误,所以直接作为参数传入
void FaceAPI::init_engine(const std::vector<int> &model_ids) {
    for (auto &model_id: model_ids) {
        if (model_id == 0) {
            initial_detector();
            FRINFO << "Init_face" << endl;
        } else if (model_id == 1) {
            initial_landmark5();
            FRINFO << "Init_land5" << endl;
        } else if (model_id == 2) {
            initial_landmark68();
            FRINFO << "Init_land68" << endl;
        } else if (model_id == 3) {
            initial_live(); //成功
            FRINFO << "Init_live" << endl;
        } else if (model_id == 4) {
            initial_facemask(); //成功
            FRINFO << "Init_faceMask" << endl;
        } else if (model_id == 5) {
            initial_age(); //成功
            FRINFO << "Init_age" << endl;
        } else if (model_id == 6) {
            initial_gender(); //成功
            FRINFO << "Init_gender" << endl;
        } else if (model_id == 7) {
            initial_mask(); //成功
            FRINFO << "Init_mask" << endl;
        } else if (model_id == 8) {
            initial_eyes(); //成功
            FRINFO << "Init_eyeState" << endl;
        } else if (model_id == 9) {
            initial_clarity(); //成功
            FRINFO << "Init_clarity" << endl;
        } else if (model_id == 10) {
            initial_bright(); //成功
            FRINFO << "Init_bright" << endl;
        } else if (model_id == 11) {
            initial_resolution(); //成功
            FRINFO << "Init_resolution" << endl;
        } else if (model_id == 12) {
            initial_pose(); //成功
            FRINFO << "Init_pose" << endl;
        } else if (model_id == 13) {
            initial_integrity(); //成功
            FRINFO << "Init_integrity" << endl;
        } else if (model_id == 14) {
            initial_tracking(); //成功
            FRINFO << "Init_faceTrack" << endl;
        } else if (model_id == 15) {
            initial_recognition(); //人脸识别
            FRINFO << "Init_recognition" << endl;
        } else {
            FRERROR << "unsupported this function,function id is" << model_id << std::endl;
        }
    }
}


//人脸框检测
SeetaFaceInfoArray FaceAPI::Detect(const SeetaImageData &simage) {
    SeetaFaceInfoArray faces = faceDetector->detect(simage);
    return faces;
}

//人脸检测阈值
void FaceAPI::SetProperty(int property, float value) {
    if (faceDetector == nullptr) {
        FRERROR << "face detector don't initial, please initial detector firstly" << std::endl;
    }
    if (property == 1) {
        faceDetector->set(seeta::FaceDetector::PROPERTY_MIN_FACE_SIZE, value); //最小人脸尺寸,默认20
    } else if (property == 2) {
        faceDetector->set(seeta::FaceDetector::PROPERTY_THRESHOLD, value); //置信度阈值
    } else if (property == 3) {
        faceDetector->set(seeta::FaceDetector::PROPERTY_MAX_IMAGE_WIDTH, value); //可检测的图像最大宽度
    } else if (property == 4) {
        faceDetector->set(seeta::FaceDetector::PROPERTY_MAX_IMAGE_HEIGHT, value); //可检测的图像最大高度
    }
}

//5特征点检测
std::vector<SeetaPointF> FaceAPI::mark5(const SeetaImageData &simage,
                                        const SeetaRect &box) {
    return landDetector5->mark(simage, box);
}

//68特征点检测
std::vector<SeetaPointF> FaceAPI::mark68(const SeetaImageData &simage,
                                         const SeetaRect &box) {
    return landDetector68->mark(simage, box);
}

void FaceAPI::SetLiveThreshold(float clarity, float reality) {
    liveDetector->SetThreshold(clarity, reality);
}

///活体检测-返回是否为活体
int FaceAPI::AliveDetect(const SeetaImageData &simage,
                         const SeetaRect &box,
                         const std::vector<SeetaPointF> &points5) {

    auto status = liveDetector->Predict(simage, box, points5.data());
    int ret = int(status);
    return ret; //=0真实,1攻击,2不确定
}

///活体检测-返回清晰度跟活体值
void FaceAPI::GetAliveScore(float *clarity, float *reality) {
    liveDetector->GetPreFrameScore(clarity, reality);
}

///视频活体检测
int FaceAPI::VideoAliveDetect(const SeetaImageData &simage,
                              const SeetaRect &box,
                              const std::vector<SeetaPointF> &points5) {
    auto status = liveDetector->Predict(simage, box, points5.data());
    int ret = int(status);
    return ret; //=0真实,1攻击,2不确定
}

///视频活体检测重置
void FaceAPI::ResetVideoAlive() {
    liveDetector->ResetVideo();
}

///五官遮挡检测,
std::vector<seeta::FaceLandmarker::PointWithMask>
FaceAPI::markMask(const SeetaImageData &simage, const SeetaRect &box) {
    return faceMaskDetector->mark_v2(simage, box);

}

///年龄检测
int FaceAPI::PredictAgeWithCrop(const SeetaImageData &simage,
                                const std::vector<SeetaPointF> &points5) {
    int age = 0;
    agePredictor->PredictAgeWithCrop(simage, points5.data(), age);
    return age;
}

int FaceAPI::PredictAge(const SeetaImageData &simage) {
    int age = 0;
    agePredictor->PredictAge(simage, age);
    return age;
}

///性别检测
int FaceAPI::PredictGenderWithCrop(const SeetaImageData &simage,
                                   const std::vector<SeetaPointF> &points5) {
    seeta::GenderPredictor::GENDER gender;
    int genderOut = 0;
    genderPredictor->PredictGenderWithCrop(simage, points5.data(), gender);
    if (gender == seeta::GenderPredictor::FEMALE)
        genderOut = 1;
    return genderOut;
}

int FaceAPI::PredictGender(const SeetaImageData &simage) {
    seeta::GenderPredictor::GENDER gender;
    int genderOut = 0;
    genderPredictor->PredictGender(simage, gender);
    if (gender == seeta::GenderPredictor::FEMALE)
        genderOut = 1;
    return genderOut;
}

///口罩检测
int FaceAPI::DetectMask(const SeetaImageData &simage, const SeetaRect &box) {
    float score = 0;
    bool mask = maskDetector->detect(simage, box, &score);
    return int(mask);
}

/// 人眼状态检测
std::vector<int> FaceAPI::DectectEye(const SeetaImageData &simage,
                                     const std::vector<SeetaPointF> &points5) {
    std::vector<int> states;
    seeta::EyeStateDetector::EYE_STATE left_eye, right_eye;
    eyeStateDetector->Detect(simage, points5.data(), left_eye, right_eye);
    states.push_back(int(left_eye));
    states.push_back(int(right_eye));
    return states;
}

/// 清晰度评估
int
FaceAPI::ClarityEvaluate(const SeetaImageData &simage, const SeetaRect &box,
                         const std::vector<SeetaPointF> &points5) {
    //低中高
    vector<int> levels = {-1, 0, 1};
    seeta::QualityResult result = qualityClarity->check(simage, box, points5.data(), 5);
    return levels[result.level];
}

/// 明亮度评估
int
FaceAPI::BrightEvaluate(const SeetaImageData &simage, const SeetaRect &box,
                        const std::vector<SeetaPointF> &points5) {
    vector<int> levels = {-1, 0, 1};
    seeta::QualityResult result = qualityBright->check(simage, box, points5.data(), 5);
    return levels[result.level];
}

/// 分辨率评估
int FaceAPI::ResolutionEvaluate(const SeetaImageData &simage, const SeetaRect &box,
                                const std::vector<SeetaPointF> &points5) {
    vector<int> levels = {-1, 0, 1};
    seeta::QualityResult result = qualityResolution->check(simage, box, points5.data(), 5);
    return levels[result.level];
}

/// 人脸姿态质量评估
int FaceAPI::PoseEvaluate(const SeetaImageData &simage, const SeetaRect &box,
                          const std::vector<SeetaPointF> &points5) {
    vector<int> levels = {-1, 0, 1};
    seeta::QualityResult result = qualityPose->check(simage, box, points5.data(), 5);
    return levels[result.level];
}

/// 人脸完整性评估
int FaceAPI::IntegrityEvaluate(const SeetaImageData &simage, const SeetaRect &box,
                               const std::vector<SeetaPointF> &points5) {
    vector<int> levels = {-1, 0, 1};
    seeta::QualityResult result = qualityIntegrity->check(simage, box, points5.data(), 5);
    return levels[result.level];
}

/// 人脸跟踪
SeetaTrackingFaceInfoArray FaceAPI::Track(const SeetaImageData &simage) {

    return faceTracker->Track(simage);
}

/// 人脸跟踪清除
void FaceAPI::ResetTrack() {
    faceTracker->Reset();
}

/// 人脸跟踪最小尺寸设置
void FaceAPI::SetTrackMinFaceSize(int facesize) {
    faceTracker->SetMinFaceSize(facesize);
}

/// 人脸跟踪器的分辨率设置
void FaceAPI::SetTrackResolution(int width, int height) {
    track_width = width;
    track_height = height;
}

/// 人脸跟踪人脸置信度设置
void FaceAPI::SetTrackThreshold(float threshold) {
    faceTracker->SetThreshold(threshold);
}

/// 人脸跟踪检测间隔
void FaceAPI::SetTrackInterval(int interval) {
    faceTracker->SetInterval(interval);
}

/// 人脸跟踪线程数设置
void FaceAPI::SetTrackThreads(int num) {
    faceTracker->SetSingleCalculationThreads(num);
}

/// 裁剪人脸
SeetaImageData FaceAPI::CropFace(const SeetaImageData &simage,
                                 const std::vector<SeetaPointF> &points5) {
    return faceRecognizer->CropFaceV2(simage, points5.data());
}

/// 裁剪图特征提取
std::vector<float> FaceAPI::ExtractCroppedFace(const SeetaImageData &simage) {
    std::vector<float> feature;
    feature.resize(1024);
    faceRecognizer->ExtractCroppedFace(simage, feature.data());
    return feature;
}

/// 原图提取特征
std::vector<float> FaceAPI::Extract(const SeetaImageData &simage,
                                    const std::vector<SeetaPointF> &points5) {
    std::vector<float> feature;
    feature.resize(1024);
    faceRecognizer->Extract(simage, points5.data(), feature.data());
    return feature;
}

/// 相似度计算
float FaceAPI::CalculateSimilarity(const std::vector<float> &feature1,
                                   const std::vector<float> &feature2) {
    float score = faceRecognizer->CalculateSimilarity(feature1.data(),
                                                      feature2.data());
    return score;
}

FaceAPI::~FaceAPI() {
    delete faceDetector;
    faceDetector = nullptr;           //人脸框
    delete landDetector5;
    landDetector5 = nullptr;        //5特征点
    delete landDetector68;
    landDetector68 = nullptr;       //68特征点
    delete liveDetector;
    liveDetector = nullptr;       //活体检测
    delete faceMaskDetector;
    faceMaskDetector = nullptr;     //五官遮挡检测
    delete agePredictor;
    agePredictor = nullptr;           //年龄预测
    delete genderPredictor;
    genderPredictor = nullptr;     //性别评估
    delete maskDetector;
    maskDetector = nullptr;           //口罩检测
    delete eyeStateDetector;
    eyeStateDetector = nullptr;   //眼睛状态检测
    delete qualityClarity;
    qualityClarity = nullptr;          //清晰度评估(传统)
    delete qualityBright;
    qualityBright = nullptr;           //明亮度评估(传统)
    delete qualityResolution;
    qualityResolution = nullptr;       //分辨率评估
    delete qualityPose;
    qualityPose = nullptr;           //姿态评估(传统)
    delete qualityIntegrity;
    qualityIntegrity = nullptr; //完整性评估
    delete faceRecognizer;
    faceRecognizer = nullptr;       //人脸识别faceFecognition
    delete faceTracker;
    faceTracker = nullptr;             //人脸跟踪器
    FRINFO << "unload engine successfully!" << endl;
}
