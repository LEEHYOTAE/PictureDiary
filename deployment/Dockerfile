FROM python:3.10

EXPOSE 8501

WORKDIR /picturediary
ADD . /picturediary

RUN pip install -r requirements.txt

COPY app.py *.so /picturediary

CMD streamlit run app.py