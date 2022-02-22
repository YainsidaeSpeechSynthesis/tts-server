@echo off
setlocal
chcp 65001
cd /D "%~dp0"
set MECAB_KO_DIC_PATH=.\mecab\mecab-ko-dic -r .\mecab\mecabrc
set TTS_MODEL_FILE=C:\YainTTS\models\yu-1.0.0\glowtts-v2\best_model.pth.tar
set TTS_MODEL_CONFIG=C:\YainTTS\models\yu-1.0.0\glowtts-v2\config.json
set VOCODER_MODEL_FILE=C:\YainTTS\models\yu-1.0.0\hifigan-v2\best_model.pth.tar
set VOCODER_MODEL_CONFIG=C:\YainTTS\models\yu-1.0.0\hifigan-v2\config.json
@REM set VOCODER_MODEL_ONNX=.\models\hifigan-v2\hifigan.onnx
server.exe
endlocal
pause