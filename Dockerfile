FROM python:3-onbuild

ENV PATH="./usr/src/app:${PATH}"
ENV SECRET_KEY="Clave"
#ENV DB_URL="postgresql://postgres:12345perro1998@127.0.0.1:5432/IMPACT"
#ENV POSTGRES_USER=test
#ENV POSTGRES_PASSWORD=test
ENV POSTGRES_USER=contact
ENV POSTGRES_PASSWORD=12345perro1998
#ENV POSTGRES_HOST=35.184.127.10
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
#ENV POSTGRES_PORT=9001
#ENV POSTGRES_DB=test
ENV POSTGRES_DB=contact

ENV MY_MAIL="xmas.suarez@gmail.com"
ENV MY_PASS="xmuidxhsducqxwbz"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "python", "impact_web_site.py" ]
