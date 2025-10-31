
local function lua_glob(path)
  local accumil = {}
  table.insert(accumil,path)
  for _,file in pairs(app.fs.listFiles(path)) do
    if file ~= "." and file ~= ".." then
      local next_path = path..'/'..file
      if app.fs.isDirectory(next_path) then
        local returned_glob = lua_glob(next_path)
        for key,value in pairs(returned_glob) do
          table.insert(accumil, value)
        end
      else
        table.insert(accumil, next_path)
      end
    end
  end
  return accumil
end

local function absolute_path(string)
  return app.fs.currentPath..'/'..string
end

local function string_to_table(string)
  local string_table = {}
  for character in string.gmatch(string,'.') do
    table.insert(string_table,character)
  end
  return string_table
end

local function flip_string(string)
  local string_table = string_to_table(string)
  local new_string = ""
  local string_length = #string_table
  for i = 1, string_length do
    local j = string_length-i+1
    new_string = new_string..string_table[j]
  end
  return new_string
end

local function get_suffix(file_path)

  local new_string_table = string_to_table(flip_string(file_path))
  local mode = 0
  local reversed_string = ""
  for key,char in pairs(new_string_table) do
    if char == '.' then
      mode = 1
    end
    if mode == 0 then
      reversed_string = reversed_string..char
    end
  end
   
  return flip_string(reversed_string)
end

local function get_basename(file_path)

  local new_string_table = string_to_table(flip_string(file_path))
  local mode = 0
  local reversed_string = ""
  for key,char in pairs(new_string_table) do
    if char == '/' then
      mode = 1
    end
    if mode == 0 then
      reversed_string = reversed_string..char
      if char == '.' then 
        reversed_string = ''
      end
    end
  end
   
  return flip_string(reversed_string)
end

local function get_parent(file_path)

  local new_string_table = string_to_table(flip_string(file_path))
  local mode = 0
  local reversed_string = ""
  for key,char in pairs(new_string_table) do
    if mode == 1 then
      reversed_string = reversed_string..char
    else
      if char == '/' then
        mode = 1
      end
    end
  end
   
  return flip_string(reversed_string)
end

local function cluster_files(files_in_folder)
  local folders = {}
  for _,value in pairs(files_in_folder) do
    if not app.fs.isDirectory(value) then
      if get_suffix(value) == 'png' then
        local key = get_parent(value)
        local elements = folders[key]
        if elements == nil then
          elements = {}
        end
        table.insert(elements, absolute_path(value))
        folders[key] = elements
      end
    end
  end
  return folders
end

local function isolate_x_y(string)
  local string_table = string_to_table(string)
  local mode = ''
  local x = ''
  local y = ''
  for _,char in pairs(string_table) do
    if char == '_' then
      mode = ''
    end
    if mode == 'x' then
      x = x..char
    elseif mode == 'y' then
      y = y..char
    end
    if char == 'x' then
      mode = 'x'
    elseif char == 'y' then
      mode = 'y'
    end
  end
  return tonumber(x),tonumber(y)
end

local function rainbow_x_y(x,y,x_max,y_max)
  local i = math.rad((x/x_max + y/y_max)*180)
  local r = (math.sin(i)+1)*127.5
  local g = (math.sin(i+120)+1)*127.5
  local b = (math.sin(i+240)+1)*127.5
  return Color{r=r,g=g,b=b,a=255}
end

local function rainbow(i)
  local ratio = 2
  local r = (math.sin(i*ratio)+1)*127.5
  local g = (math.sin(i*ratio+120)+1)*127.5
  local b = (math.sin(i*ratio+240)+1)*127.5
  return Color{r=r,g=g,b=b,a=255}
end

local function clump(folders)
  for key,value in pairs(folders) do
    local x_cell,y_cell = isolate_x_y(get_basename(key))
    local sprites = #value
    local y_length = math.ceil(math.sqrt(sprites))
    local x_length = math.ceil(sprites/y_length)
    local y = y_cell * y_length
    local x = x_cell * x_length
    local sprite = Sprite(x,y)
    local x_iter = 0 
    local y_iter = 0
    local count = 0
    for key2,value2 in pairs(value) do
      local sprite_2 = app.Open(value2)
      

      local rectangle = Rectangle(x_iter,y_iter, x_cell, y_cell)
      local slice = sprite:newSlice(rectangle)
      slice.name = value2

      slice.color = rainbow_x_y(x_iter,y_iter,x,y)
      x_iter = x_iter + x_cell
      count = count + 1
      if x_iter == x then
        x_iter = 0
        y_iter = y_iter + y_cell
      end
    end
    sprite:saveAs(key..'/'..x..'_'..y..'.aseprite')
  end
end

local function clump_2(files)
  for key,value in pairs(files) do
    if not app.fs.isDirectory(value) then
      if get_suffix(value) == 'png' then
        local x_cell,y_cell = isolate_x_y(get_basename(get_parent(value)))
        local x_iter = 0
        local y_iter = 0
        local count = 0
        print(value)
        local ref_path = (get_parent(value)..'/'..get_basename(value)..'.txt')
        local ref_strings = {}
        for line in io.lines(ref_path) do
          local accumil = ""
          for char in string.gmatch(line,'.') do
            if char ~= '\n' then
              accumil = accumil..char
            end
          end
          table.insert(ref_strings,accumil)
        end
        local x, y = isolate_x_y(get_basename(value))

        local sprite = app.open(value)
        for _,value2 in pairs(ref_strings) do
          

          local rectangle = Rectangle(x_iter,y_iter, x_cell, y_cell)
          local slice = sprite:newSlice(rectangle)
          slice.name = value2

          slice.color = rainbow_x_y(x_iter,y_iter,x,y)
          x_iter = x_iter + x_cell
          count = count + 1
          if x_iter == x then
            x_iter = 0
            y_iter = y_iter + y_cell
          end
        end
        print(1)
        sprite:saveAs('renamed'..'/x'..x_cell..'_y'..y_cell..'/'..get_basename(value)..'.aseprite')
        print(2)
      end
    end
  end
end


local files = lua_glob('renamed')
clump_2(files)
