fid = fopen('pic_name.txt');
fidout = fopen('pic_out.txt','w+');
y=0;
while feof(fid) ==0
    tline = fgetl(fid);
    num = length(tline);
    str = strsplit(tline,',');
    strout = str{1};
    for i = 2:length(str)
        if mod(i,2)==1
        else
            strout = strcat(strout,',',str{i});
        end
    end
    fprintf(fidout,'%s\n',strout);
end
fclose(fid);
fclose(fidout);
