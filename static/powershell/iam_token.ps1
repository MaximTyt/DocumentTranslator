$yandexPassportOauthToken = "y0_AgAAAAAb1THTAATuwQAAAADeLGJ48ULVUspDQqeYQmlUgeNb0LM-3ZY"
$Body = @{ yandexPassportOauthToken = "$yandexPassportOauthToken" } | ConvertTo-Json -Compress
Invoke-RestMethod -Method 'POST' -Uri 'https://iam.api.cloud.yandex.net/iam/v1/tokens' -Body $Body -ContentType 'Application/json' | Select-Object -ExpandProperty iamToken