addpath('D:\Projects\HarpDB\matlab');

clear conn data cur 

% connect to database
conn = database('HarpDB', 'harp-user', '-OrejadeVanG0gh-', 'Server',...
    'sei.ucsd.edu', 'Vendor', 'MySQL');

% example queries TODO

% selects all deployments of a certain project and site (in this case
% CINMSB)
com = 'select Data_ID, Latitude, Longitude, Depth_m, Data_Start_Date, Data_End_Date, Rec_Dur,PreAmp from harp_data_summary_4 where Data_ID regexp ''CINMS[0-9_-]+[B].*''';
% example of query with hardcoded names
% com = 'select Data_ID, Latitude, Longitude, Depth_m, Data_Start_Date, Data_End_Date, Rec_Dur,PreAmp from harp_data_summary_4 where Data_ID IN (''CINMS_B_34'',''CINMS_B_36'')';
cur = exec(conn, com);
cur = fetch(cur);
data = cur.Data;

lats = zeros(1, size(data, 1));
lons = zeros(1, size(data, 1));
names = cell(1, size(data, 1));
desc = cell(1, size(data, 1));
recTimes = zeros(size(data,1),2);
preAmp = cell(1,size(data,1));

% loop through each entry
for i = 1:size(data, 1)
    lat = char(data(i, 2));
    lon = char(data(i, 3));
    try
        [lat, lon] = lat_lon_conv(lat, lon);
    catch ME
        fprintf('Whoops you''re fucked: %s\n', ME.message);
        lats(i) = [];
        lons(i) = [];
        names(i) = [];
        desc(i) = [];
        continue
    end
    lats(i) = lat;
    lons(i) = lon;
    names{i} = char(data(i, 1));
%     desc{i} = ['Recording duration: ' , char(cell2mat(data(i, 4))), ' days']; % TODO
    desc{i} = sprintf('%s to %s\n%s days\nz = %.0f meters', char(data{i,5}), char(data{i,6}), ...
        data{i,7}, data{i,4});
    preAmp{i} = data{i,8};
    fprintf('%s\t\t%.4f\t\t%.4f\t\tz =\t%.0f\n',data{i,1},lat,lon,data{i,4});
    try 
        recTimes(i,1) = datenum(cur.Data{i,5});
        recTimes(i,2) = datenum(cur.Data{i,6});
    catch ME
        fprintf('\tNo data start/end times: %s\n', ME.message);
    end
end

offn = 'D:\Projects\ShippingCINMS\code\matlab\CINMS_B_depInfo.mat';

% list of deployments to exclude
exDeps = {
    'CINMS_B_30_0115'; % non standard deployment
    'CINMS_B_30_0130'; % non standard deployment
    'CINMS_B_30_0145'; % non standard deployment
    'CINMS_B_30_03';   % non standard deployment
    'CINMS_B_30_0515'; % non standard deployment
    'CINMS_B_30_0530'; % non standard deployment
    'CINMS_B_30_0545'; % non standard deployment
    'CINMS_B_32';      % bad hydrophone
    };

% exclude deployments before saving query
fprintf('Excluding deployments:\n');
for exi = 1:length(exDeps) 
    fprintf('\t%s\n',exDeps{exi});
    rmi = find(strcmp(names,exDeps{exi}));
    desc(rmi) = [];
    lats(rmi) = [];
    lons(rmi) = [];
    names(rmi) = [];
    recTimes(rmi,:) = [];
    preAmp(rmi) = [];    
end

save(offn,'lats','lons','names','desc','recTimes','preAmp');

1;

