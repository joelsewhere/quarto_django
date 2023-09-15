import sys
import nbformat

# read notebook from stdin
nb = nbformat.reads(sys.stdin.read(), as_version = 4)


for index, cell in enumerate(nb.cells):
    if cell.cell_type == 'code':
        outputs = []
        for output in cell.outputs:
            text = output.get('data', {}).get('text/html', '') + output.get('text', '')
            if 'site-packages' in text or 'INFO' in text:
                continue
            else:
                outputs.append(output)
        cell.outputs = outputs
    
  
# write notebook to stdout 
nbformat.write(nb, sys.stdout)
