# Ödev 5 kontrolü: odev5.py'yi çalıştırır, her görevin çıktısını beklenen çıktıyla karşılaştırır.
# PyCharm'da bu dosyayı açıp Run deyin. odev5.py ile aynı klasörde olmalı. Not vermez, yol gösterir.
# odev5.py geçici bir klasörde çalışır; sizin transcript.txt ve fal.txt dosyalarınıza dokunulmaz.
# Görev 5'te ad olarak Mehmet yazılır. Fincan penceresi açılmaz: turtle komutları yalnızca sayılır.
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ODEV = HERE / "odev5.py"
NAME = "Mehmet"

EXPECTED = {
    "1. Dersi bul": ["FIZ127 3 kredi", "EEM101 transkriptte yok"],
    "2. Kelime sayma": ["bir 3", "berber 2", "11 kelime, 8 farklı kelime"],
    "3. Alfabenin harfleri": ["29 harf", "0 harf eksik", "17 harf eksik", "8 ortak harf",
                              "19 farklı harf"],
    "4. Not dökümü dosyası": ["{'MAT123': 'C1', 'FIZ127': 'B2', 'BBM101': 'A3', 'TKD103': 'A2'}",
                              "4 ders", "transcript_2025.txt bulunamadı", "0 ders"],
    # Görev 5: önce a ve b'nin test satırları, sonra programın çıktısı (aşağıda ayrıca bakılır)
    "5. Kahve falı": ["sağ üst", "sol üst", "sol alt", "sağ alt", "sağ üst", "sol alt", "sağ üst"],
}
OPTIONAL = {"Meraklısına": ["1 fal, 1 kişi"]}
TRANSCRIPT_LINES = ["MAT123;4;C1", "FIZ127;3;B2", "BBM101;3;F3", "TKD103;2;A2", "BBM101;3;A3"]
FORTUNE_LINE = re.compile(r"Telvenin çoğu (sağ üst|sol üst|sol alt|sağ alt) çeyrekte: (\d+) tane\.")
TELVE_RADIUS = 130
DOT_COUNT = 100

# Ek denemeler: function'lar test satırlarındakinden başka değerlerle de çağrılır.
# (görev, function, argument'lar, beklenen sonuç, ekrana yazması beklenen)
EXTRA_FILE = "EEM101;4;F2\nFIZ137;3;C2\nEEM101;4;A1\n"
EXTRA = [
    ("1.", "find_credits", ([("TKD103", 2, "A2"), ("EEM101", 4, "B1")], "EEM101"), "4", ""),
    ("1.", "find_credits", ([("TKD103", 2, "A2")], "MAT123"), "None", ""),
    ("3.", "letters_of", ("Kahve falı 2026!",), "{'a', 'e', 'f', 'h', 'k', 'l', 'v', 'ı'}", ""),
    ("4.", "read_grades", ("ek_deneme.txt",), "{'EEM101': 'A1', 'FIZ137': 'C2'}", ""),
    ("4.", "read_grades", ("olmayan.txt",), "{}", "olmayan.txt bulunamadı"),
    ("5.", "find_quarter", (0, -5), "'sağ alt'", ""),
    ("5.", "find_quarter", (-1, 0), "'sol üst'", ""),
    ("5.", "find_quarter", (7, 0), "'sağ üst'", ""),
    ("5.", "busiest_quarter", ({"sağ üst": 5, "sol üst": 9, "sol alt": 9, "sağ alt": 1},),
     "'sol üst'", ""),
    ("5.", "busiest_quarter", ({"sağ üst": 0, "sol üst": 0, "sol alt": 0, "sağ alt": 1},),
     "'sağ alt'", ""),
]

# Sık görülen error message'lar için kısa ipuçları: (mesajda geçen, görev, ipucu)
HINTS = [
    ("'dict' object has no attribute 'add'", "", "{} boş bir dict'tir; boş set'i set() ile kurun."),
    ("'set' and 'list'", "", "letters_of() bir set return etmeli; -, & ve | iki set arasında "
                             "çalışır."),
    ("KeyError", "", "dict'te olmayan bir key okundu. Sayarken ilk turda key yoktur: "
                     "get(key, 0) kullanın."),
    ("write() argument must be str", "", "write() yalnızca str alır; sayıyı f-string ile yazın."),
    ("'NoneType'", "", "Bir yerde None ile işlem yapılıyor. Bir function sonucu print ediyor ama "
                       "return etmiyor olabilir."),
    ("values to unpack", "4.", "Her satır split(\";\") ile üç parçaya bölünmeli. transcript.txt'ye "
                               "yazarken her satırın sonuna \"\\n\" eklediniz mi, okurken "
                               "strip() kullandınız mı?"),
    ("values to unpack", "", "Unpacking'de isim sayısı, açılan tuple'ın eleman sayısıyla aynı "
                             "olmalı."),
    ("FileNotFoundError", "", "Okunmak istenen dosya yok. Dosyayı yazan görevi bitirdiniz mi, "
                              "adını doğru yazdınız mı?"),
    ("EOFError", "", "input() birden çok kez çağrılıyor; Görev 5'te adı yalnızca bir kez sorun."),
]

# odev5.py'yi bu küçük programın içinde çalıştırıyoruz: turtle'ın yerine noktaları sayan
# sahte bir turtle koyar, input()'a yazılan adı Run penceresindeki gibi ekrana da yazar.
RUNNER = r'''
import ast
import builtins
import contextlib
import io
import json
import sys
import types

odev, calls_path, record_path = sys.argv[1:4]
record = {"dots": [], "done": False, "fortunes": None, "results": []}
position = [0, 0]


def goto(x, y=None):
    if y is None:
        x, y = x
    position[0], position[1] = x, y


def dot(*args):
    record["dots"].append([position[0], position[1]])


def done():
    record["done"] = True


class Anything:
    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, name):
        return self


fake = types.ModuleType("turtle")
fake.goto = fake.setpos = fake.setposition = fake.teleport = goto
fake.dot = dot
fake.done = fake.mainloop = fake.exitonclick = done
fake.__getattr__ = lambda name: Anything()
sys.modules["turtle"] = fake


def echo_input(prompt=""):
    sys.stdout.write(str(prompt))
    line = sys.stdin.readline()
    if not line:
        raise EOFError("EOF when reading a line")
    line = line.rstrip("\r\n")
    print(line)
    return line


builtins.input = echo_input


def show(value):
    if isinstance(value, set):
        return "{" + ", ".join(sorted(repr(x) for x in value)) + "}" if value else "set()"
    return repr(value)


def attempt(namespace, name, args):
    func = namespace.get(name)
    if not callable(func):
        return {"missing": True}
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            value = func(*args)
    except Exception as error:
        return {"error": type(error).__name__ + ": " + str(error), "printed": buffer.getvalue()}
    return {"value": show(value), "printed": buffer.getvalue()}


with open(odev, encoding="utf-8-sig") as f:
    source = f.read()
namespace = {"__name__": "__main__", "__file__": odev, "__builtins__": builtins}
try:
    exec(compile(source, odev, "exec"), namespace)
    fortunes = namespace.get("FORTUNES")
    if isinstance(fortunes, dict):
        record["fortunes"] = {str(k): [str(x) for x in v] for k, v in fortunes.items()
                              if isinstance(v, list)}
    with open(calls_path, encoding="utf-8") as f:
        calls = ast.literal_eval(f.read())
    for name, args in calls:
        record["results"].append(attempt(namespace, name, args))
finally:
    with open(record_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False)
'''


def sections(text):
    """'=== başlık ===' satırlarına göre çıktıyı böler."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.fullmatch(r"=== (.+) ===", line.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line.rstrip())
    return out


def block(src, start, end):
    """odev5.py'de iki görev başlığı arasındaki kod (comment satırları hariç)."""
    a = src.find(start)
    if a == -1:
        return ""
    b = src.find(end, a + 1) if end else len(src)
    lines = src[a:b if b != -1 else len(src)].splitlines()[1:]
    return "\n".join(ln for ln in lines if ln.strip() and not ln.strip().startswith("#"))


def compare(have, want):
    """İlk farklı satırı söyler; hepsi aynıysa None döner."""
    for i, w in enumerate(want):
        h = have[i] if i < len(have) else "(satır yok)"
        if h != w:
            return f"{i + 1}. satır beklenen: {w!r}, sizinki: {h!r}"
    if len(have) > len(want):
        return f"beklenenden fazla satır var: {have[len(want)]!r}"
    return None


def opens_without_encoding(code):
    """encoding="utf-8" yazılmadan açılan file'lar."""
    found = []
    for m in re.finditer(r"\bopen\(", code):
        depth, i = 1, m.end()
        while i < len(code) and depth:
            depth += {"(": 1, ")": -1}.get(code[i], 0)
            i += 1
        call = code[m.start():i]
        if not re.search(r"encoding\s*=\s*[\"']utf-8[\"']", call, re.IGNORECASE):
            found.append(" ".join(call.split()))
    return [f'file\'ı encoding="utf-8" ile açın: {call}' for call in found]


def quarter_of(x, y):
    """Görevdeki kural: x = 0 sağ, y = 0 üst sayılır."""
    return ("sağ" if x >= 0 else "sol") + " " + ("üst" if y >= 0 else "alt")


def extra_notes(task, results):
    """Ek denemelerden kalanlar."""
    notes = []
    for (t, name, args, want, want_printed), res in zip(EXTRA, results):
        if t != task or res.get("missing"):
            continue
        call = f"{name}({', '.join(repr(a) for a in args)})"
        if "error" in res:
            notes.append(f"ek deneme {call} hata verdi: {res['error']}")
        elif res["value"] != want:
            notes.append(f"ek deneme {call} beklenen: {want}, sizinki: {res['value']}")
        elif res["printed"].strip() != want_printed:
            notes.append(f"ek deneme {call} ekrana {want_printed!r} yazmalı, "
                         f"sizinki: {res['printed'].strip()!r}")
    if task == "4." and notes:
        notes.append("ek_deneme.txt'de EEM101 iki kez geçiyor, önce F2, sonra A1; son not geçerli")
    return notes


def check_task1(code, run):
    notes = []
    if "def find_credits(" not in code:
        notes.append("find_credits(transcript, code) adlı function'ı yazın")
    elif not re.search(r"return\s+None\b", code):
        notes.append("ders transkriptte yoksa None'ı açıkça return edin: return None")
    return notes


def check_task2(code, run):
    notes = []
    if ".lower()" not in code or ".split()" not in code:
        notes.append("text'i lower() ile küçük harfe çevirip split() ile words list'ine ayırın")
    if ".get(" not in code:
        notes.append("derste gördüğümüz sayma kalıbını kullanın: "
                     "word_counts[word] = word_counts.get(word, 0) + 1")
    if ".items()" not in code:
        notes.append("birden çok geçen kelimeleri items() ile dolaşarak yazdırın")
    if "len(" not in code or re.search(r"[\"'][^\"'\n]*\d[^\"'\n]*[\"']", code):
        notes.append("çıktıdaki sayıları kendiniz yazmayın: len() ve dict'teki sayılar versin")
    return notes


def check_task3(code, run):
    notes = []
    if not re.search(r"range\(\s*len\(\s*alphabet\s*\)\s*\)", code) or ".add(" not in code:
        notes.append("alphabet_set'i for, range(len(alphabet)) ve add() ile kurun")
    if "def letters_of(" not in code:
        notes.append("letters_of(sentence) adlı function'ı yazın")
    elif ".lower()" not in code:
        notes.append("letters_of() cümleyi önce lower() ile küçük harfe çevirmeli")
    return notes


def check_task4(code, run):
    notes = []
    content = run["transcript"]
    wanted = "".join(line + "\n" for line in TRANSCRIPT_LINES)
    if content is None:
        notes.append('transcript.txt yazılmadı: "w" ile açıp lines\'taki her satırı yazın')
    elif content != wanted:
        if content.replace("\n", "") == "".join(TRANSCRIPT_LINES):
            notes.append('transcript.txt\'de satırlar ayrılmamış: her satırın sonuna "\\n" ekleyin')
        else:
            notes.append(f"transcript.txt beklenen gibi değil, ilk satırları: "
                         f"{content.splitlines()[:2]}")
    if code.count("MAT123;4;C1") > 1:
        notes.append("satırları kendiniz yazmayın: lines list'ini for ile dolaşın")
    if "def read_grades(" not in code:
        notes.append("read_grades(file_name) adlı function'ı yazın")
    else:
        if ".strip()" not in code or not re.search(r"split\(\s*[\"'];[\"']\s*\)", code):
            notes.append("her satırı strip() ile temizleyip split(\";\") ile parçalara ayırın")
        if not re.search(r"except\s+FileNotFoundError", code):
            notes.append("file yoksa program durmasın: open()'ı try ile sarıp "
                         "except FileNotFoundError ile yakalayın")
    notes += opens_without_encoding(code)
    return notes


def check_task5(code, run, have):
    notes = []
    want = EXPECTED["5. Kahve falı"]
    start = next((i for i, ln in enumerate(have) if ln.startswith("Adınız")), len(have))
    tests, program = have[:start], have[start:]
    if not tests:
        notes.append("a ve b'nin test satırlarının çıktısı yok: function'ları yazıp test "
                     "satırlarını açın")
    else:
        diff = compare(tests, want)
        if diff:
            if len(tests) < len(want):
                diff += " (a ve b'nin test satırlarının hepsini açtınız mı?)"
            notes.append("a ve b'nin test satırları: " + diff)
    if "def find_quarter(" not in code:
        notes.append("a) find_quarter(x, y) adlı function'ı yazın")
    if "def busiest_quarter(" not in code:
        notes.append("b) busiest_quarter(counts) adlı function'ı yazın")
    elif ".items()" not in code:
        notes.append("b) busiest_quarter() çeyrekleri items() ile dolaşmalı")
    if not program:
        notes.append('c) programın çıktısı yok: adı input("Adınız: ") ile sorarak başlayın')
        return notes
    notes += check_program(program, run)
    if not re.search(r"\bwhile\b", code):
        notes.append("c) noktaları while ile serpin")
    if code.count("DOT_COUNT") < 2:
        notes.append("c) 100'ü kendiniz yazmayın, DOT_COUNT'u kullanın")
    if not re.search(r"open\([^)]*[\"']a[\"']", code):
        notes.append('c) fal.txt\'yi "a" ile açın; "w" her çalıştırmada eski falları siler')
    notes += opens_without_encoding(code)
    return notes


def check_program(program, run):
    """Görev 5c: fal rastgele olduğu için satırların biçimine ve sayının doğruluğuna bakılır."""
    notes = []
    fixed = {0: f"Adınız: {NAME}", 2: f"{NAME}, falınız şöyle:",
             4: "Bu fal, fal.txt dosyasının sonuna eklendi.",
             5: "Falınıza bir sayaç ile bir if baktı; tutarsa tesadüf."}
    for i, w in fixed.items():
        h = program[i] if i < len(program) else "(satır yok)"
        if h != w:
            notes.append(f"c) programın {i + 1}. satırı beklenen: {w!r}, sizinki: {h!r}")
    if len(program) > 6:
        notes.append(f"c) programın çıktısında fazla satır var: {program[6]!r}")
    line = program[1] if len(program) > 1 else ""
    m = FORTUNE_LINE.fullmatch(line)
    if not m:
        notes.append("c) programın 2. satırı şu biçimde olmalı: "
                     f"'Telvenin çoğu sol alt çeyrekte: 40 tane.', sizinki: {line!r}")
    dots = run["record"]["dots"]
    inside = [(x, y) for x, y in dots if x ** 2 + y ** 2 < TELVE_RADIUS ** 2]
    if len(dots) != DOT_COUNT:
        notes.append(f"c) fincana {len(dots)} nokta kondu; turtle.dot() ile DOT_COUNT kadar, "
                     f"yani {DOT_COUNT} nokta konmalı")
    if len(inside) != len(dots):
        notes.append("c) fincanın dışına da nokta konmuş: önce noktanın fincanın içinde olup "
                     "olmadığını if ile sınayın, sonra goto() ve dot()")
    if m and dots:
        counts = {}
        for x, y in dots:
            counts[quarter_of(x, y)] = counts.get(quarter_of(x, y), 0) + 1
        quarter, number = m.group(1), int(m.group(2))
        if number != counts.get(quarter, 0):
            notes.append(f"c) {quarter} çeyreğine {counts.get(quarter, 0)} nokta düştü ama "
                         f"çıktıda {number} yazıyor; sayıyı quarter_counts[busiest]'ten alın")
        elif number != max(counts.values()):
            notes.append(f"c) en kalabalık çeyrek {quarter} değil: noktalar {counts}")
    fortune = program[3] if len(program) > 3 else ""
    fortunes = run["record"]["fortunes"]
    if m and fortunes and fortune not in fortunes.get(m.group(1), []):
        notes.append(f"c) fal, FORTUNES[\"{m.group(1)}\"] içindeki üç faldan biri olmalı, "
                     f"sizinki: {fortune!r}")
    fal = run["fal"]
    if fal is None:
        notes.append('c) fal.txt yazılmadı: falı "a" ile fal.txt\'nin sonuna ekleyin')
    elif fal != f"{NAME}: {fortune}\n":
        notes.append(f"c) fal.txt'de beklenen satır: {NAME + ': ' + fortune!r} ve sonunda \"\\n\", "
                     f"sizinki: {fal!r}")
    if not run["record"]["done"]:
        notes.append("c) en sona turtle.done() yazın")
    return notes


def run_odev():
    """odev5.py'yi geçici bir klasörde çalıştırır; çıktıyı ve yazdığı file'ları toplar."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "kontrol_runner.py").write_text(RUNNER, encoding="utf-8")
        (tmp / "ek_deneme.txt").write_text(EXTRA_FILE, encoding="utf-8")
        (tmp / "ek_denemeler.txt").write_text(repr([(n, a) for _, n, a, _, _ in EXTRA]),
                                              encoding="utf-8")
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        proc = subprocess.run(
            [sys.executable, "kontrol_runner.py", str(ODEV), "ek_denemeler.txt", "kayit.json"],
            cwd=tmp, input=NAME + "\n", capture_output=True, text=True, encoding="utf-8",
            errors="replace", env=env, timeout=20)

        def read(name):
            path = tmp / name
            return path.read_text(encoding="utf-8", errors="replace") if path.exists() else None

        record = json.loads(read("kayit.json") or "{}")
        record.setdefault("dots", [])
        record.setdefault("done", False)
        record.setdefault("fortunes", None)
        record.setdefault("results", [])
        return {"proc": proc, "record": record, "transcript": read("transcript.txt"),
                "fal": read("fal.txt")}


def main():
    if not ODEV.exists():
        print("odev5.py bulunamadı. kontrol.py ile aynı klasöre koyun.")
        return
    try:
        run = run_odev()
    except subprocess.TimeoutExpired:
        print("odev5.py 20 saniyede bitmedi. Bitmeyen bir while olabilir: Görev 5'te serpilen "
              "noktaları sayan sayacı her turda artırdınız mı?")
        return
    proc = run["proc"]
    print(f"odev5.py çalıştırıldı: ad olarak {NAME} yazıldı, fincan penceresi açılmadı.\n")
    if proc.returncode != 0:
        last = [ln for ln in proc.stderr.splitlines() if ln.strip()]
        last = last[-1] if last else "(boş)"
        print("odev5.py çalışırken hata verdi. Error message'ın son satırı:")
        print("   ", last)
        where = [n for path, n in re.findall(r'File "(.*)", line (\d+)', proc.stderr)
                 if path.endswith("odev5.py")]
        if where:
            print(f"Hatanın olduğu satır: odev5.py, {where[-1]}. satır")
        headers = re.findall(r"^=== (.+) ===$", proc.stdout, re.MULTILINE)
        task = headers[-1] if headers else ""
        if task:
            print(f"Hata bu görevde çıktı: {task}")
        for key, in_task, hint in HINTS:
            if key in last and task.startswith(in_task):
                print("İpucu:", hint)
                break
        print("Önce bu hatayı düzeltin, sonra kontrolü tekrar çalıştırın.")
        return
    got = sections(proc.stdout)
    src = ODEV.read_text(encoding="utf-8-sig")
    starts = ['print("=== 1.', 'print("=== 2.', 'print("=== 3.', 'print("=== 4.',
              'print("=== 5.', 'print("=== Meraklısına']
    checks = [check_task1, check_task2, check_task3, check_task4]
    passed = 0
    for n, (title, want) in enumerate(EXPECTED.items()):
        have = got.get(title)
        if have is None:
            print(f"✗ {title}: başlık satırı çıktıda yok. Başlığı yazdıran print() satırını silmeyin.")
            continue
        code = block(src, starts[n], starts[n + 1])
        if not have:
            notes = ["çıktı yok: TODO'yu doldurun"]
            if n != 1:
                notes[0] += ", sonra test satırlarını seçip Ctrl+/ (macOS: Cmd+/) ile açın"
        elif n == 4:
            notes = check_task5(code, run, have)
        else:
            diff = compare(have, want)
            notes = ([diff] if diff else []) + checks[n](code, run)
        if not notes:
            notes = extra_notes(title[:2], run["record"]["results"])
        if notes:
            print(f"✗ {title}")
            for note in notes:
                print("    " + note)
        else:
            print(f"✓ {title}")
            passed += 1
    for title, want in OPTIONAL.items():
        have = got.get(title, [])
        if have:
            print(("✓ " if have == want else "· ") + title + " (zorunlu değil)")
    print(f"\n{passed} / {len(EXPECTED)} görev geçti.")


main()
