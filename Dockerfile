FROM localstack/localstack:2.3

# Enable only S3
ENV SERVICES=s3
ENV DEBUG=1

# Copy analyzer report
COPY report.json /tmp/report.json

# Copy init script to official ready hook directory
COPY init-s3.sh /etc/localstack/init/ready.d/init-s3.sh

# Ensure executable permissions
RUN chmod +x /etc/localstack/init/ready.d/init-s3.sh

EXPOSE 4566