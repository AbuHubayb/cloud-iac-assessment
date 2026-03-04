# Pull LocalStack as base_image
FROM localstack/localstack:2.2

# Enable S3
ENV SERVICES=s3
ENV DEBUG=1

# Copy report into container
COPY report.json /tmp/report.json

# Expose LocalStack port
EXPOSE 4566

# Start LocalStack, create bucket, upload report
CMD ["bash", "-c", "\
localstack start --host & \
sleep 5 && \
awslocal s3 mb s3://analyzer-reports && \
awslocal s3 cp /tmp/report.json s3://analyzer-reports/report.json && \
tail -f /dev/null \
"]