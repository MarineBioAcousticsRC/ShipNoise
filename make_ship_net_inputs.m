% Script that matches times of passages with closest sound speed profile.
% Also computes harmonic mean sound speed and saves both to file along with
% image (save both range and time versions), associated vectors and ship properties.
trainingOutputFolder = 'M:\ShipNoise_nnet_input_CASE_only';
if ~isfolder(trainingOutputFolder)
    mkdir(trainingOutputFolder)
end
catVecAll = [];
hMeanAll = [];
myProfileAll = [];
allPassDateStr = [];

shipLib = [ 0,0
          31,1 % towing
          32,1 % towing
          52,1 %Tug
          70,2 % Cargo
          71,2% Cargo
          72,2 % Cargo
          74,2% Cargo
          77,2% Cargo
          79,2% Cargo
          80,3 % Tanker
          82,3 % Tanker
        1004,2 % cargo
        1005,4 % industrial
        1010,5 % offshore supply
        69, 6  % passenger
        1012,6 % passenger
        1019,7 % recreational
        1020,0 % research
        1024,3 % tanker
        1025,1] %tug
    

    
% load sound speed profiles
load('J:\CASE_only.mat')
headersData = importdata('J:\VZDATAALL_CorrectedSL_AllSD.csv');
    
addData = readtable('J:\VZDATAALL_CorrectedSL_AllSD.csv');%% haven't added this yet
myHeaders = strsplit(strrep(headersData.textdata{1},'.','_'),',');
addData.Properties.VariableNames = cellstr(myHeaders(1:end-1));


shipPassList = dir('M:\MarineCadastre\Monthly4500mTrackAboutCPA_KF\**\*.mat');
sspSet_pruned = sspSet(all(~cellfun(@isempty,struct2cell(sspSet)))); % remove empty rows.
nPass = length(shipPassList);
for iPass = 1:nPass
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
    if mean(mean(thisPassage))<60 ||isnan(mean(mean(thisPassage)))
        fprintf('too quiet, skipping %0.0f\n',iPass)
        continue
    end
    thisDraught = abs(myPass.thisShipTrack.vData(1,3));
    thisLength = myPass.thisShipTrack.vData(1,4)+myPass.thisShipTrack.vData(1,5);
    thisWidth = myPass.thisShipTrack.vData(1,6)+myPass.thisShipTrack.vData(1,7);
    thisCPA = min(myPass.xResize);
    if thisCPA>6000
        continue
    end
    thisTonnage = 0;
    [~,cpaIdx] = min(abs(thisCPA-myPass.thisShipTrack.range));
    if ~isempty(matchIdx)
        if addData.draught(matchIdx(1))>0
            thisDraught = addData.draught(matchIdx(1));
        else 
            1;
        end
        if addData.shipLength(matchIdx(1))<500
            thisLength = addData.shipLength(matchIdx(1))*3.28;
        else
            1;
        end
        %thisTonnage = addData.GT(matchIdx(1));
        thisHP = addData.Total_HP_Main_Eng(matchIdx(1));
    end
    try
        thisSOG = mean(myPass.thisShipTrack.SOG(cpaIdx-5:cpaIdx+5));
    catch
        fprintf('failed on CPA index, file %0.0f\n',iPass')
        continue
    end
    thisCOG = mean(myPass.thisShipTrack.COG(cpaIdx-5:cpaIdx+5));
    thisHeading = mean(myPass.thisShipTrack.trueHeading(cpaIdx-5:cpaIdx+5));
    if thisHeading>360
        thisHeading = thisHeading-360;
    end
    thisShipTemp = str2num(myPass.thisShipTrack.shipType{1});
    if ~isempty(thisShipTemp)
        thisShipType = shipLib((shipLib(:,1) == thisShipTemp),2);
    else
        thisShipType = 0;
    end
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
        thisDraught = 0;
    elseif thisCPA>5000
        thisCPA = addData.CPADist(matchIdx(1));
    end
    passDateStr = datestr(myPass.thisShipTrack.dnums(1),'yymmddHHMMSS');
    outName = sprintf('%0.0f_%s.mat',myPass.thisShipTrack.MMSI,passDateStr);
    catVecAll= [catVecAll;catVec];
    hMeanAll = [hMeanAll,thisHmean];
    myProfileAll = [myProfileAll,thisProfile];
    allPassDateStr = [allPassDateStr;passDateStr];
    thisPassage(1,:) = thisDistVec/100;
    %thisPassage(2,:) = thisDistVec/100;
    %thisPassage(3,:) = thisDistVec/100;
    MMSI = myPass.thisShipTrack.MMSI;
    passDate = myPass.thisShipTrack.dnums(1);
    save(fullfile(trainingOutputFolder,outName),...
        'thisDistVec','thisPassage','thisDraught','thisLength','thisWidth',...
        'thisCPA','thisTonnage','thisSOG','thisCOG','thisHeading','thisShipType',...
        'MMSI','thisProfile','thisHmean','passDate','-v7.3');
end
 
% thisWidth =[5,200] % typical ranges.
% thisLength = [20,1000]
% thisDraught = [1,15]%
% CPA = [2000,4500]%
% Norm scheme for thisHeading should be: thisHeading - 180/[-180,180]
% Norm scheme for thisCOG should be: thisCOG - 180/[-180,180]
% thisSOG = [5,20];
[dateSet,IX] = sort(datenum(allPassDateStr,'yymmddHHMMSS'));
figure(11);clf
hIm = imagesc(dateSet,1:200,myProfileAll(:,IX))

%hIm = imagesc(myProfileAll);
%datetick('x','mmm-yy','keepLimits')
cH = colorbar;
ylabel('Depth (m)')
xlabel('Date')
cHy = ylabel(cH,'Sound Speed (m/s)');
set(cHy,'Rotation',-90)