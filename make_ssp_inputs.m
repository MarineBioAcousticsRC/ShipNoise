% Script that matches times of passages with closest sound speed profile.
% Also computes harmonic mean sound speed and saves both to file along with
% image (save both range and time versions), associated vectors and ship properties.
dCINMSB = 580; % assume site depth is this
% load sound speed profiles
sspCSV = 'J:\CALCOFI_NO_UCSB_SPRAY_CASE.csv';
sspDataName = 'J:\CASE_only.mat';

T = importdata(sspCSV);
addpath('E:\Code\GSW\')
%%
nanRows = isnan(T.data(:,3));
T.data(nanRows,:) = [];
T.textdata(nanRows,:) = [];
idStr = [];
iSet = 1;
myTimes = [];
Tkeep = [];
for iS = 1:length(T.textdata)
    if ~strcmp(T.textdata{iS,2} ,'CASE')
        continue
    end
    if strcmp(T.textdata{iS,5},'2')||strcmp(T.textdata{iS,5},'3')
        T.textdata{iS,5} = '1';
    end
    
    idStr{iSet,1} = sprintf('%s_%s_%s',T.textdata{iS,2},T.textdata{iS,3},T.textdata{iS,5});
    %myTimes = [myTimes;datenum(T.textdata{iS,3})];
    Tkeep.data(iSet,:) = T.data(iS,:);
    Tkeep.textdata(iSet,:) = T.textdata(iS,:);    
    
    iSet = iSet+1;

end
[uR,iA,iC] = unique(idStr);%,'rows');
uRowIdxSort = sort(iA);
myDepths = 1:200;

%%
CT = Tkeep.data(:,2);
PR = Tkeep.data(:,1);% equating Pressure to depth, not quite right...
SA = Tkeep.data(:,3);
sound_speed = gsw_sound_speed(SA,CT,PR);
Tkeep.data(:,4) = sound_speed;

sspSet = struct;
for iU = 1:size(uRowIdxSort,1)-1
    %thisProfile = T.data(uRowIdxSort(iU):(uRowIdxSort(iU+1)-1),:);
    profIdxs = find(iC==iU);
    thisProfile = Tkeep.data(profIdxs,:);
    
    thisProfileText = Tkeep.textdata(profIdxs,:);
    if size(thisProfile,1)<25 %||iU == 895;
        continue
    end
    [~,uR] = unique(thisProfile(:,1));
    thisProfile = thisProfile(uR,:);
    resampledProfile = interp1(thisProfile(:,1),thisProfile(:,4),myDepths,'linear','extrap')';
    sspSet(iU).profile = resampledProfile;
    try
        sspSet(iU).datenum = datenum(thisProfileText(1,3),'dd-mmm-yy');
    catch
        sspSet(iU).datenum = datenum(thisProfileText(1,3),'yyyymmdd');
    end
    sspSet(iU).datetxt = thisProfileText(1,3);
    H = sndspd_mean(myDepths',resampledProfile,dCINMSB);
    sspSet(iU).harmMeanSSP = H;

end
[tSort,IX] = sort([sspSet(:).datenum]);
sspSet = sspSet(IX);
imagesc([sspSet.profile])
plot([sspSet.datenum],[sspSet.harmMeanSSP])
%sspDataName = strrep(sspCSV,'.csv','.mat');
save(sspDataName,'sspSet','-v7.3')
