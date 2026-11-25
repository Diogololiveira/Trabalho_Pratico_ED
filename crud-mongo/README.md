CRUD MongoDB
 
Mapeamento das 16 tabelas do esquema universidade para MongoDB:
13 coleções + leciona, alocacao e cursa em turma.
 
## Como executar
```bash
cd crud-mongo
python -m venv venv && source venv/bin/activate   # no windows seria venv\Scripts\activate
pip install -r requirements.txt
# crie o .env na raiz com: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, MONGO_URI, MONGO_DB
python setup_schema.py      # cria coleções, validadores e índices 
python migrar_dados.py      # copia os dados do Postgre
python main.py              # CRUD de usuário, estudante, curso e vínculo
```
