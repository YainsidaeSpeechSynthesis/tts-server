@echo off
setlocal
chcp 65001
cd /D "%~dp0"
set MECAB_KO_DIC_PATH=.\mecab\mecab-ko-dic -r .\mecab\mecabrc
set TTS_MODEL_FILE=.\models\glowtts-v2\checkpoint_30000.pth.tar
set TTS_MODEL_CONFIG=.\models\glowtts-v2\config.json
set VOCODER_MODEL_FILE=.\models\hifigan-v2\checkpoint_300000.pth.tar
set VOCODER_MODEL_CONFIG=.\models\hifigan-v2\config.json
@REM set VOCODER_MODEL_ONNX=.\models\hifigan-v2\hifigan.onnx
server.exe
endlocal
pause