
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
      local key = get_parent(value)
      local elements = folders[key]
      if elements == nil then
        elements = {}
      end
      table.insert(elements, absolute_path(value))
      folders[key] = elements
    end
  end
  for key,value in pairs(folders) do
    print(key)
    for key2,value2 in pairs(value) do
      print("    ",value2)
    end
  end
end

local files = lua_glob("renamed")
cluster_files(files)
print('done')
