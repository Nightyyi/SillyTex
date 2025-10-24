# NewLayer

```lua
app.command.NewLayer {
  name=string,
  group=bool,
  reference=bool,
  tilemap=bool,
  gridBounds=Rectangle,
  ask=bool,
  fromFile=bool,
  fromClipboard=bool,
  viaCut=bool,
  viaCopy=bool,
  top=bool,
  before=bool
}
```

* `name` (string): the name of the layer.
* `group`: `true` to make the new layer a group layer, this option is mutually exclusive with `reference`/`tilemap`.
* `reference`: `true` to make the new layer a reference layer, this option is mutually exclusive with `group`/`tilemap`.
* `tilemap`: `true` to make the new layer a tilemap layer, this option is mutually exclusive with `group`/`reference`.
* `gridBounds`: a [rectangle](../rectangle.md#rectangle) to specify the tilemap grid by default (instead of using the sprite grid)
* `ask`: `true` to ask the user for a name if inside the interface.
* `fromFile`: `true` to create the layer from a file, the Open File dialog will appear in the UI.
* `fromClipboard`: `true` to create the layer from clipboard image data.
* `viaCut`: `true` the selected image data is cut and moved into the new layer.
* `viaCopy`: `true` the selected image data is copied into the new layer.
* `top`: `true` the newly created layer is placed at the top of the list.
* `before`: `true` the newly created layer is placed before the currently active layer; but if false it is placed after.
