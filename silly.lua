local lfs = require"lfs"

print('hello world')
local list = {'this is a table i think',"hiii"};
for key,value in pairs(list) do
print(key,value);
end


local function lua_glob(path)
  local accumil = {}
  table.insert(accumil,path)
  for file in lfs.dir(path) do
    if file ~= "." and file ~= ".." then
      local next_path = path..file
      local attr = lfs.attributes (next_path)
      if type(attr) ~= 'nil' then
        if attr.mode == "directory" then
          local returned_glob = lua_glob(next_path)
          for key,value in pairs(returned_glob) do
            table.insert(accumil, value)
          end
        end
      else
        table.insert(accumil, next_path)
      end
    end
  end
  return accumil
end

local n = lua_glob("renamed/")
for i,value in pairs(n) do
  print(i, value)
end
