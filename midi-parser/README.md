# MIDI PARSER

Uses the `Music21` library.


<br/>

## Run

```
python main.py
```


<br/>

## Import

```python
from parse_midi import MIDI_Converter
```


<br/>

## Parsing

First of all, create an instance of the `MIDI_Converter`.  
This could look as the following.
```python
MC = MIDI_Converter()
```

You can now start converting **single files** using:
```python
result = MC.convert("<inset_file_path_here>")
```

Or convert **all MIDI files** of a folder:
```python
results = MC.convertFiles("<inset_folder_path_here>")
```


<br/>

## Result Structure

After parsing a **single file** successfully, you will receive an object of the following structure:
```
{
  'success': True,
  'filename' <filename_without_path>,
  'data'
  [
    {
      'type': 'note' / 'chord',
      'name': <str>,
      'octave': <int> (type=note only),
      'pitch': <str> (type=note only),
      'duration': <str>,
      'notes': [] (<int> values, type=chord only)
    }
  ]
}
```

After parsing **multiple files** of a folder successfully, you will receive:
```
{
  'success': True,
  'data':
  [
    {
      'filename': <str> (without path),
      'filepath': <str> (filepath and name),
      'data':
      [
        { @see above (data part of single file) },
        { ... },
        ...
      ]
    },
    { ... },
    ...
  ]
}
```
