
# Move ./tests directory to parent directory
Move-Item -Path .\tests -Destination ..
Move-Item -Path .\unitest -Destination ..

# Publish to pypi
flit publish --repository pypi --pypirc C:\Users\green\.pyirc

# Move back the "tests" directory from parent directory to current directory
Move-Item -Path ..\tests -Destination .
Move-Item -Path ..\unitest -Destination .

# wait for pypi to update
Write-Host "waiting 10 seconds for pypi to update"
Start-Sleep -Seconds 10

# Update metaffi-api pip package
py -m pip install metaffi-api --upgrade