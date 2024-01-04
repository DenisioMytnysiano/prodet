FROM bitnami/spark:3.5.0

RUN pip install install translators spacy_fastlang keras tensorflow tensorflow_hub pandas pyarrow nltk
RUN python -m spacy download en_core_web_sm 
RUN python -m nltk.downloader stopwords -d /tmp/ntlk

CMD /opt/bitnami/spark/sbin/start-connect-server.sh --packages org.apache.spark:spark-connect_2.12:3.5.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.kafka:kafka-clients:3.5.0
