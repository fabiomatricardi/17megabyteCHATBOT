#!/bin/bash

# Step 1:
# Check if docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: docker is not installed.' >&2
  exit 1
fi
# Step 2:
# Check if we have already built the image
if [[ "$(docker images -q faqbot 2> /dev/null)" == "" ]]; then
  echo 'Building the image'
  # Step 3:
  # Build image and add a descriptive tag
  docker build -f Dockerfile . -t faqbot
fi
# Step 4:
# Run the gradio app
docker run -ti  -p 7860:7860  --rm faqbot 