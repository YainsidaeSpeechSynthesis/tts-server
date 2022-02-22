import json

a = {
    "name": "나레이션 양반",
    "description": "나레이션 양반",
}
b = [
    {
        "name": "염동진",
        "description": "야인시대 염동진",
        "latest_version": "1.0.0",
        "code": "yu",
        "versions": [
            {
                "version": "1.0.0",
                "description": "염동진의 첫 버전",
                "download_url": "https://github.com/YainsidaeSpeechSynthesis/Yeom-Dongjin/releases/download/1.0.0/yu-1.0.0.zip"
            }
        ],
        "repository": "https://github.com/YainsidaeSpeechSynthesis/Yeom-Dongjin"
    },
    {
        "name": "나레이션 양반",
        "description": "야인시대 나레이션 양반",
        "latest_version": "1.0.0-beta.1",
        "code": "na",
        "versions": [
            {
                "version": "1.0.0-beta.1",
                "description": "나레이션 양반의 첫 버전",
                "download_url": "https://github.com/YainsidaeSpeechSynthesis/Narration-Yangban/releases/download/1.0.0-beta.1/na-1.0.0-beta.1.zip"
            }
        ],
        "repository": "https://github.com/YainsidaeSpeechSynthesis/Narration-Yangban"
    }
]
c= json.dumps(b)
print(c)