% M = csvread(filename,R1,C1)
%
% C = textscan(fileID,'%0.0f %f %f %f %f ','Delimiter', ',')
% R1 = 1;C1 = 1;
% R2 = 1000; C2=1;
% M = dlmread('F:\AIS_2017_04_Zone11\AIS_ASCII_by_UTM_Month\2017\AIS_2017_04_Zone11.csv',',',[R1 C1 R2 C2]);
siteB = [ 34.2755, -120.0185 ];

rlat = siteB(1) * pi/180;
% Ref: American Practical Naviagator, Bowditch 1958, table 6 (explanation)
% page 1187
m = 111132.09 - 566.05 * cos(2*rlat) + 1.2 * cos(4*rlat) - 0.003 * cos(6*rlat);
p = 111415.10 * cos(rlat) - 94.55 * cos(3*rlat) - 0.12 * cos(5*rlat);


% for starters, let's filter for any ships inside some lat/lon box
boundd_m = 15e3; % in [m]
maxLat = [ siteB(1)-boundd_m/m, siteB(1)+boundd_m/m ];
maxLon = [ siteB(2)-boundd_m/p, siteB(2)+boundd_m/p ];

fclose all;
fList = dir('E:\Downloads\AIS_zone10\AIS_ASCII_by_UTM_Month\2016\*.csv ');
for iFile = 1:size(fList,1)
    saveName = fullfile(fList(iFile).folder,strrep(fList(iFile).name,'.csv','_CINMS.mat'));
    if exist(saveName,'file')
        continue
    end
    fileID = fopen(fullfile(fList(iFile).folder,fList(iFile).name));
    myLatRange = [34,34.5];
    myLonRange = [-120.8,-119.6];
    tLine = fgetl(fileID);
    thisMMSI = NaN;
    itr = 1;
    
    MCset.MMSI = [];
    MCset.lat = [];
    MCset.lon = [];
    MCset.time = [];
    MCset.SOG = [];
    MCset.COG = [];
    MCset.heading = [];
    MCset.type = {};
    MCset.name = {};
    MCset.length = [];
    MCset.width = [];
    MCset.draught = [];
    while ~feof(fileID)
        tLine = fgetl(fileID);
        myFields = regexp(tLine,',','split');
        thisLat = str2double(myFields{3});
        thisLon = str2double(myFields{4});
        if thisLat> maxLat(1) && thisLat< maxLat(2)&&...
                thisLon> maxLon(1) && thisLon< maxLon(2)
            MCset.MMSI(itr,1) = str2double(myFields{1});
            MCset.lat(itr,1) = thisLat;
            MCset.lon(itr,1) = thisLon;
            MCset.time(itr,1) = datenum(myFields{2},'yyyy-mm-ddTHH:MM:SS');
            MCset.SOG(itr,1) = str2double(myFields{5});
            MCset.COG(itr,1) = str2double(myFields{6});
            MCset.heading(itr,1) = str2double(myFields{7});
            MCset.type (itr,1) = cellstr(myFields{11});
            MCset.name{itr,1} =  cellstr(myFields{8});
            MCset.length(itr,1) = str2double(myFields{13});
            MCset.width(itr,1) = str2double(myFields{14});
            MCset.draught(itr,1) = str2double(myFields{15});
            disp('got one');
            itr = itr+1;
        end
        
    end
    
    fclose(fileID)
    
    save(saveName,'MCset','-v7.3')
    fprintf('Done saving %s\n',saveName)
end