from django.core.management import call_command
from io import StringIO

output = StringIO()
call_command('dumpdata',
             exclude=['contenttypes', 'auth.permission'],
             indent=2,
             stdout=output)

with open("data.json", "w", encoding="utf-8") as f:
    f.write(output.getvalue())

print("✅ Dump complete and saved as UTF-8.")
