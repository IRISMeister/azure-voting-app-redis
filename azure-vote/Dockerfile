FROM store/intersystems/iris-community:2020.3.0.221.0 AS build-env
FROM tiangolo/uwsgi-nginx-flask:python3.6
COPY --from=build-env /usr/irissys/dev/python/irisnative-1.2.0-cp34-abi3-linux_x86_64.whl .
RUN pip install irisnative-1.2.0-cp34-abi3-linux_x86_64.whl
ADD /azure-vote /app
