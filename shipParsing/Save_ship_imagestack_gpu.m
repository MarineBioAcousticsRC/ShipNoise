clearvars

addpath('E:\Code\SPICE-box\SPICE-Detector\io')
addpath('E:\Code\SPICE-box\SPICE-Detector\funs')
tfDir = 'E:\TFs';
outDir = 'F:\ShippingCINMS_data';
folderTag = 'COP';
mainDir = fullfile(outDir,folderTag);
dirList = dir(fullfile(mainDir,'2*'));

imageStackAll = [];
shipTypeAll = {};
IMOAll = [];
shipSizeAll = [];
draughtAll = [];
tfList = importdata('F:\ShippingCINMS_data\CINMS_TFs.csv');
tic
speedAtRMSAll = [];
rangeAtRMSAll = [];
rmsEAll = [];
makeImages = 1
dataStore = struct;
iC = 1;
for iDir = 1:length(dirList)
    subDir = fullfile(dirList(iDir).folder,dirList(iDir).name);
    fList = dir(fullfile(subDir,'*.wav'));
    nFiles = size(fList,1);
    imageStack = [];
    
    iCStart = iC;
    iR = 1;
    for iFile = 1:nFiles
        draught = [];
        IMO = [];
        shipType = [];
        CPADist = [];
        transitDateTime = [];
        meanSOG = [];
        shipSize = [];
        MMSI = [];
        siteName = [];
        tfFile = [];
        
        
        p.DateRegExp = '_(\d{6})_(\d{6})';
        soundFile = fullfile(fList(iFile).folder,fList(iFile).name);
        % check if text file exists
        txtFile = strrep(soundFile,'.wav','.txt');
        
        if ~exist(txtFile,'file')
            warning('Could not find file %s, skipping.','txtFile')
            continue
        end
        
        hdr = io_readWavHeader(soundFile,p.DateRegExp);
        wavData = io_readWav(soundFile,hdr,...
            1,(hdr.xhd.byte_length/hdr.samp.byte), 'Normalize','unscaled');
        if makeImages
            
            wavData1 = gpuArray(wavData);
        end
        
        % get associated info from text file
        textData = importdata(txtFile);
        
        if ~isfield(textData,'textdata')
            textTemp = textData;
            textData = struct;
            textData.textdata = textTemp;
        end
        
        [siteName,~] = regexp(textData.textdata{1,1},'HARPSite=(\w*)','tokens','match');
        siteName = siteName{1};
        
        tfIdx = find(~cellfun(@isempty,strfind(tfList.textdata(:,1),siteName)));
        tfNum = tfList.data(tfIdx-1);
        tfFolder = dir(fullfile(tfDir,[num2str(tfNum),'*']));
        tfFile = dir(fullfile(tfFolder.folder,tfFolder.name,'*.tf'));
        
        k1Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'ShipType'))==1);
        if ~isempty(k1Idx)
            [k1,~]= regexp(textData.textdata{k1Idx,1},'ShipType=(\w*)','tokens','match');
            shipType = k1{1,1};
        end
        k2Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'IMO='))==1);
        if ~isempty(k2Idx)
            k2Idx = k2Idx(1);% hit a case with 2 IMO#s ??
            [k2,~]= regexp(textData.textdata{k2Idx,1},'IMO=(\d*)','tokens','match');
            IMO = str2double(char(k2{1,1}));
        end
        k3Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'toBow'))==1);
        if ~isempty(k3Idx)
            [k3,~]= regexp(textData.textdata{k3Idx,1},'toBow\[m\]=(\d*.\d*)','tokens','match');
            shipSize = str2num(char(k3{1,1}));
        end
        k4Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'Draught'))==1);
        if ~isempty(k4Idx)
            [k4,~]= regexp(textData.textdata{k4Idx,1},'Draught\[m\]=(\d*\.\d*)','tokens','match');
            draught = str2num(char(k4{1,1}));
        end
        
        k5Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'CPADistance'))==1);
        if ~isempty(k5Idx)
            [k5,~]= regexp(textData.textdata{k5Idx,1},'CPADistance\[m\]=(\d*)','tokens','match');
            CPADist = str2num(char(k5{1,1}));
        end
        k6Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'CPATime'))==1);
        if ~isempty(k6Idx)
            [k6,~]= regexp(textData.textdata{k6Idx,1},'(\d*/\d*/\d*\W\d*:\d*:\d*)','tokens','match');
            transitDateTime = datenum(k6{1,1});
        end
        k7Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'MMSI='))==1);
        if ~isempty(k7Idx)
            [k7,~]= regexp(textData.textdata{k7Idx,1},'MMSI=(\d*)','tokens','match');
            MMSI = str2double(k7{1,1});
        end
        if isfield(textData,'data') && size(textData.data,2)>3
            meanSOG = mean(textData.data(:,4));
        end
        
        
        if makeImages
            
            [specOut,fOrig,t] = makeSpectrogram(wavData);
            
            [~, uppc] = fn_tfMap(fullfile(tfFile.folder,tfFile.name),fOrig);
            if isempty(uppc)
                error('missing tf file')
            end
            specMat = gather(specOut)+repmat(uppc,1,size(specOut,2));
            specMatTruncHF = specMat(5:1600,:);
            f = fOrig(5:1600);
            
            F = griddedInterpolant(specMatTruncHF);
            [sx,sy,sz] = size(specMatTruncHF);
            log10sx = log10(sx);
            log10sxVec = (0:(log10sx/1024):log10sx);
            log10xq = 10.^(log10sxVec(2:end));
            
            % logsx = log(sx);
            % logsxVec = (1:(logsx/1024):logsx);
            % logxq = exp(logsxVec(2:end))';
            
            yq = (0:sy/1024:sy)';
            % if size(yq,1)==1023
            %    yq = (.5:sy/1024:sy)';
            %  end
            xq = (1:sx/1024:sx)';
            myPassageLog10 = F({log10xq(:,:),yq});
            myPassage = F({xq,yq});
            fInterp = interp1(f,xq);
            fLog10 = interp1(f,log10xq)';
            imageStack(:,:,iR) = myPassageLog10;
            dataStore(iC).fLog10 = fLog10;
            dataStore(iC).f = f;
            dataStore(iC).t = t;
        end
        % logvq = F({logxq(:,:),yq});
        % vq = F({xq,yq});
        saveName = strrep(soundFile,'.wav','_spectrogram.mat');
        
        dataStore(iC).fileName = saveName;
        dataStore(iC).soundFile = soundFile;
        dataStore(iC).textFile = txtFile;
        dataStore(iC).draught = draught;
        dataStore(iC).IMO = IMO;
        dataStore(iC).shipType = shipType;
        dataStore(iC).CPADist = CPADist;
        dataStore(iC).transitDateTime = transitDateTime;
        dataStore(iC).meanSOG = meanSOG;
        dataStore(iC).shipSize = shipSize;
        dataStore(iC).MMSI = MMSI;
        dataStore(iC).HarpSite = siteName;
        dataStore(iC).TFFile = tfFile;
        
        if strcmp(shipType,'Tanker')
         [speedAtRMS,rangeAtRMS,rmsE] = test_rangeVsRL(wavData,textData,hdr);
            speedAtRMSAll = [speedAtRMSAll;speedAtRMS];
            rangeAtRMSAll = [rangeAtRMSAll;rangeAtRMS];
             rmsEAll = [rmsEAll;rmsE'];
        end
        passageData = dataStore(iC);
        if 0%makeImages
            save(saveName, 'myPassageLog10','specMatTruncHF','myPassage','passageData','f',...
                'saveName','soundFile','txtFile','draught','IMO','shipType','fLog10',...
                'CPADist','transitDateTime','meanSOG','shipSize','MMSI',...
                'siteName','tfFile','-v7.3');
        end
        iC = iC+1;
        iR = iR+1;
    end
    
    % prune out empty IMO, which seems to mean no auxiliary info
    %     keepers = IMO~=0;
    %     imageStack = imageStack(:,:,keepers);
    %     shipType = shipType(keepers);
    %     IMO = IMO(keepers);
    %     shipSize = shipSize(keepers);
    %     draught = draught(keepers);
    
    %     imageStackAll = cat(3,imageStackAll,imageStack);
    %     shipTypeAll = [shipTypeAll;shipType];
    %     IMOAll = [IMOAll;IMO];
    %     shipSizeAll = [shipSizeAll;shipSize];
    %     draughtAll = [draughtAll;draught];
    if makeImages
        subSetData = dataStore(iCStart:iC-1);
        save(fullfile(outDir,[folderTag,'_monthStack_',dirList(iDir).name]),...
            'imageStack','subSetData','-v7.3')
    end
    fprintf('done with folder %s',subDir)
end
toc
%save(fullfile(outDir,'folderTag_combinedPassageData.mat'),'dataStore')

function [sdB,f,t] = makeSpectrogram(data)

overlap = 0;
nfft = 10e3;
noverlap = 0;%(overlap/100)*nfft;
fs = 10e3;

% this seems to match the plot made by spectrogram with y-axis option
[~,f,t,psd] = spectrogram(data,hanning(nfft),noverlap,nfft,fs,'psd');
sdB = 10*log10(psd);


end
