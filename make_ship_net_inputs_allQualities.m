% Script that matches times of passages with closest sound speed profile.
% Also computes harmonic mean sound speed and saves both to file along with
% image (save both range and time versions), associated vectors and ship properties.
trainingOutputFolder = 'M:\ShipNoise_nnet_input_v3';
if ~isdir(trainingOutputFolder)
    mkdir(trainingOutputFolder)
end
catVecAll = [];
hMeanAll = [];
myProfileAll = [];
allPassDateStr = [];
% load sound speed profiles
load('J:\CALCOFI_UCSB_SPRAY_CASE.mat')
headersData = importdata('J:\VZDATAALL_CorrectedSL_AllSD.csv');
    
addData = readtable('J:\VZDATAALL_CorrectedSL_AllSD.csv');%% haven't added this yet
myHeaders = strsplit(strrep(headersData.textdata{1},'.','_'),',');
addData.Properties.VariableNames = cellstr(myHeaders(1:end-1));
shipPassList = dir('M:\MarineCadastre\Monthly4500mTrackAboutCPA_KF\**\*.mat');
sspSet_pruned = sspSet(all(~cellfun(@isempty,struct2cell(sspSet)))); % remove empty rows.
nPass = length(shipPassList);
for iPass = 1623:nPass
    myPass = load(fullfile(shipPassList(iPass).folder,shipPassList(iPass).name),...
        'xResize','yResize','sdBRadon','thisShipTrack');
    if ~isfield(myPass,'xResize')
        fprintf('Skipping file %0.0f: %s\n', iPass,...
            fullfile(shipPassList(iPass).folder,shipPassList(iPass).name))
        continue
    end
    
   
    % match date:
    [minVal,minIdx] = min(abs(myPass.thisShipTrack.dnums(1)-[sspSet.datenum]));
    
    thisProfile = sspSet_pruned(minIdx).profile;
    thisHmean =  sspSet_pruned(minIdx).harmMeanSSP;
     matchIdx = find(strncmp(addData.txtFile,shipPassList(iPass).name,length(shipPassList(iPass).name)-9));
    if isempty(matchIdx)
        1;
    end
    thisDistVec = myPass.xResize;
    thisPassage = myPass.sdBRadon(2:end-1,2:end-1);
    thisDraught = myPass.thisShipTrack.vData(1,3);
    thisLength = myPass.thisShipTrack.vData(1,4)+myPass.thisShipTrack.vData(1,5);
    thisWidth = myPass.thisShipTrack.vData(1,6)+myPass.thisShipTrack.vData(1,7);
    thisCPA = min(myPass.xResize);
    thisTonnage = [];
    [~,cpaIdx] = min(abs(thisCPA-myPass.thisShipTrack.range));
    if ~isempty(matchIdx)
        thisDraught = addData.draught(matchIdx(1));
        thisLength = addData.shipLength(matchIdx(1));
        thisTonnage = addData.GT(matchIdx(1));
        thisHP = addData.Total_HP_Main_Eng(matchIdx(1));
    end
    try
        thisSOG = mean(myPass.thisShipTrack.SOG(cpaIdx-5:cpaIdx+5));
    catch
        fprintf('failed on CPA index, file %0.0f\n',iPass')
        continue
    end
    thisCOG =  mean(myPass.thisShipTrack.COG(cpaIdx-5:cpaIdx+5));
    thisHeading =  mean(myPass.thisShipTrack.trueHeading(cpaIdx-5:cpaIdx+5));
    thisShipType = str2num(myPass.thisShipTrack.shipType{1});
    catVec = [thisShipType,thisTonnage,thisLength,thisDraught,thisCPA,thisHeading,thisCOG,thisSOG];
    if isnan(sum(catVec))||length(catVec)<8
        fprintf('has nans, skipping file %0.0f\n',iPass')
        1;
        continue
        
    end
    
    if length(thisProfile)~=200
        1;
    elseif thisCOG>360
        1;
    elseif thisSOG<4
        1;
    elseif thisWidth<1|| thisWidth>300
        1;
    elseif thisDraught<1
        1;
    elseif thisCPA>5000
        thisCPA = addData.CPADist(matchIdx(1))
    end
    passDateStr = datestr(myPass.thisShipTrack.dnums(1),'yymmddHHMMSS');
    outName = sprintf('%0.0f_%s.mat',myPass.thisShipTrack.MMSI,passDateStr);
    catVecAll= [catVecAll;catVec];
    hMeanAll = [hMeanAll,thisHmean];
    myProfileAll = [myProfileAll,thisProfile];
    allPassDateStr = [allPassDateStr;passDateStr];
%     save(fullfile(trainingOutputFolder,outName),...
%         'thisDistVec','thisPassage','thisDraught','thisLength','thisWidth',...
%         'thisCPA','thisTonnage','thisSOG','thisCOG','thisHeading','thisShipType',...
%         'thisProfile','thisHmean','thisHP','-v7.3');
end
 
% thisWidth =[5,200] % typical ranges.
% thisLength = [20,1000]
% thisDraught = [1,15]%
% CPA = [2000,4500]%
% Norm scheme for thisHeading should be: thisHeading - 180/[-180,180]
% Norm scheme for thisCOG should be: thisCOG - 180/[-180,180]
% thisSOG = [5,20];