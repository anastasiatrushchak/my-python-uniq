import click
import sys

def get_input_iter(filepath):
    """Відкриває stdin або файл для читання."""
    if filepath == '-':
        return sys.stdin
    else:
        try:
            return open(filepath, 'r', encoding='utf-8')
        except FileNotFoundError:
            sys.stderr.write(f"myuniq: неможливо відкрити '{filepath}' для читання: Файл не знайдено\n")
            sys.exit(1)

def get_output_writer(filepath):
    """Відкриває stdout або файл для запису."""
    if filepath == '-':
        return sys.stdout
    else:
        try:
            return open(filepath, 'w', encoding='utf-8')
        except Exception as e:
            sys.stderr.write(f"myuniq: Помилка відкриття файлу для запису: {e}\n")
            sys.exit(1)

def process_group(line, count, writer, show_count, duplicates_only, unique_only):
    """Виводить попередню групу рядків на основі прапорів."""
    if line is None: 
        return

    should_print = False
    if duplicates_only and count > 1:
        should_print = True
    elif unique_only and count == 1:
        should_print = True
    elif not duplicates_only and not unique_only:
        should_print = True
    
    if should_print:
        prefix = f"{count: >7} " if show_count else ""
        writer.write(f"{prefix}{line}")

@click.command()
@click.option('-c', '--count', 'show_count', is_flag=True, help='Показувати кількість повторень.')
@click.option('-d', '--repeated', 'duplicates_only', is_flag=True, help='Виводити тільки рядки, що повторюються.')
@click.option('-u', '--unique', 'unique_only', is_flag=True, help='Виводити тільки унікальні рядки.')
@click.argument('input_file', type=click.Path(allow_dash=True), default='-')
@click.argument('output_file', type=click.Path(allow_dash=True), default='-')
def main(show_count, duplicates_only, unique_only, input_file, output_file):
    """
    Python-реалізація команди uniq.
    
    Фільтрує суміжні однакові рядки з INPUT (або stdin),
    записуючи в OUTPUT (або stdout).
    
    ПРИМІТКА: `myuniq` працює, лише якщо однакові рядки йдуть підряд.
    Для повного аналізу файлу спочатку відсортуйте його:
    
    sort somefile.txt | myuniq
    """
    if duplicates_only and unique_only:
        sys.stderr.write("myuniq: опції --unique та --repeated є взаємовиключними\n")
        sys.exit(1)

    input_iter = get_input_iter(input_file)
    writer = get_output_writer(output_file)

    prev_line = None
    count = 0

    try:
        for line in input_iter:
            if line == prev_line:
                count += 1
            else:
                process_group(prev_line, count, writer, show_count, duplicates_only, unique_only)

                prev_line = line
                count = 1
        
        process_group(prev_line, count, writer, show_count, duplicates_only, unique_only)

    except Exception as e:
        sys.stderr.write(f"myuniq: Помилка: {e}\n")
    finally:
        if input_iter is not sys.stdin:
            input_iter.close()
        if writer is not sys.stdout:
            writer.close()

if __name__ == '__main__':
    main()