# Start by building the application.
FROM golang:1.15 as build

WORKDIR /go/src/app
COPY . /go/src/app

RUN CGO_ENABLED=0 go build -o /go/bin/server

# Now copy it into our base image.
FROM gcr.io/distroless/base
COPY --from=build /go/bin/server /
CMD ["/server"]
