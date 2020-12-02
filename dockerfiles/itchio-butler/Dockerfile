FROM amazon/aws-cli:2.1.4 as installer 

RUN yum install -y unzip && \
  curl -L -o butler.zip https://broth.itch.ovh/butler/linux-amd64/LATEST/archive/default && \
  unzip butler.zip -d /bin/butler && \
  chmod +x /bin/butler/butler

FROM amazonlinux:2
COPY --from=installer /bin/butler /bin/butler
COPY --from=installer /usr/local/aws-cli/ /usr/local/aws-cli/
COPY --from=installer /usr/local/bin/ /usr/local/bin/
ENV PATH="$PATH:/bin/butler:/usr/local/aws-cli:/usr/local/bin"
COPY ./push-game.sh .
RUN yum install -y unzip && chmod +x push-game.sh

CMD ["butler", "-V"]