inDir = dir('F:\ShippingCINMS_data\rangeFreqSpectrograms_COP_ALL\*.mat');
HARPLat=34.27553;
HARPLon=-120.01853;
load('E:\Downloads\AIS_zone10\AIS_ASCII_by_UTM_Month\2016\AIS_2016_02_Zone10_CINMS.mat')
% load('F:\MarineCadastre\csvs\AIS_2016_01_Zone11_CINMS.mat');
stringMatch = strfind({inDir.name},'_1601')';
thisMonthSet = find(~cellfun(@isempty,stringMatch));
thisMonthSet(cell2mat(stringMatch(thisMonthSet))~=10) = [];
dnum2 = datenum([0,0,0,0,30,0]);
figure(17); colormap(jet)
offTime = [];
offSetVal = [];
for iFile = 1:length(thisMonthSet)
    inFile = fullfile(inDir(thisMonthSet(iFile)).folder,inDir(thisMonthSet(iFile)).name);
    myPassage = load(inFile);
    try 
        thisShipIdx = find(MCset.MMSI==myPassage.MMSI);
    catch
        disp('no MMSI')
        continue
    end
    MCTime = MCset.time(thisShipIdx);
    
    SBCPA = myPassage.CPATime;
    [SIOTime,UI] = unique(myPassage.timeSteps);
    % prune out passages that are not within 2 hours of SB CPA
    badTimes = find(MCTime<(SBCPA - dnum2)|MCTime>(SBCPA + dnum2));
    MCTime(badTimes) = [];
    thisShipIdx(badTimes) = [];
    [MCTime,UIMC] = unique(MCTime);
    thisShipIdx = thisShipIdx(UIMC);
    CAll = zeros(size(myPassage.shipLat));
    IminAll = zeros(size(myPassage.shipLat));
    if isempty(thisShipIdx)
        disp('Vessel passage not found')
        continue
    end
    sioTimeInterp = min(myPassage.timeSteps): (1/(24*60*60)):max(myPassage.timeSteps);
    sioLatInterp = interp1(SIOTime,myPassage.shipLat(UI),sioTimeInterp);
    sioLonInterp = interp1(SIOTime,myPassage.shipLon(UI),sioTimeInterp);
    
    MCLatInterp = interp1(MCTime,MCset.lat(thisShipIdx),sioTimeInterp);
    MCLonInterp = interp1(MCTime,MCset.lon(thisShipIdx),sioTimeInterp);
        
    
    [xRangeSIO,yRangeSIO] = latlon2xy(HARPLat,HARPLon,sioLatInterp,sioLonInterp);
    rangeSIO  = sqrt(xRangeSIO.^2+yRangeSIO.^2);

    [xRangeMC,yRangeMC] = latlon2xy(HARPLat,HARPLon,MCLatInterp,MCLonInterp);
    rangeMC  = sqrt(xRangeMC.^2+yRangeMC.^2);

%     
%     for iRow = 1:length(myPassage.shipLat)
%         % interpolate to common time
%         
%         [C,Imin] = min(sum(abs([myPassage.shipLat(iRow),myPassage.shipLon(iRow)]-...
%             [MCset.lat(thisShipIdx),MCset.lon(thisShipIdx)]),2));
%         CAll(iRow) = C;
%         IminAll(iRow) = Imin;
%     end
%     [overallMin,overallMinIdx] = min(CAll);
%     
%     syncTimeSB = myPassage.timeSteps(overallMinIdx);
%     syncTimeMC = MCTime(IminAll(overallMinIdx));
%     %     [thisTimeSorted, IX] = sort(thisTime);
%     %     thisTime = datestr(thisTimeSorted);
%     %     thisLat = MCset.lat(thisShipIdx(IX));
%     %     thisLon = MCset.lon(thisShipIdx(IX));
%     offBy = datevec(abs(syncTimeSB-syncTimeMC));
%     
%     
%     if size(myPassage.shipLat,1)~=size(myPassage.timeSteps,1)
%         continue
%     end
    % disp([num2str(abs(syncTimeSB-syncTimeMC)),'\n'])
       
    if 1%abs(syncTimeSB-syncTimeMC)>datenum([0,0,0,0,3,0])
%         clf
%         scatter(sioTimeInterp,rangeMC,25,sioTimeInterp,'x')
%         hold on
%         scatter(sioTimeInterp,rangeSIO,6,sioTimeInterp,'o')
%         set(gca,'clim',[min(sioTimeInterp),max(sioTimeInterp)])
%         datetick('x','MM:SS')
%         1;
%         hold off
%         
        [~,CPASIOIdx] = min(rangeSIO);
        [~,CPAMCIdx] = min(rangeMC);
        offSetVal = [offSetVal;(sioTimeInterp(CPASIOIdx)-sioTimeInterp(CPAMCIdx))];
        offTime =  [offTime;min(sioTimeInterp)];
    end
    %outFile = strrep(inFile,'.mat','_tAdjust.mat');
    %offset_sec_SBminusMC = (syncTimeMC-syncTimeSB)*24*60*60; 
    % If MC time is before our time, then adjustment time will be negative,
    % indicating that our time should be adjusted backward.
    %save(outFile,'offset_sec_SBminusMC','-v7.3')
end

