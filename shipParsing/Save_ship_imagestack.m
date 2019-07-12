addpath('E:\Code\SPICE-box\SPICE-Detector\io')


mainDir = 'J:\ShippingCINMS_data\COP';
dirList = dir(fullfile(mainDir,'2*'));

imageStackAll = [];
shipTypeAll = {};
IMOAll = [];
shipSizeAll = [];
draughtAll = [];

tic
for iDir = 2%:length(dirList)
    subDir = fullfile(dirList(iDir).folder,dirList(iDir).name);
    fList = dir(fullfile(subDir,'*.wav'));
    nFiles = size(fList,1);
    imageStack = zeros(1024,1025,nFiles);
    shipType = cell(nFiles,1);
    IMO = zeros(nFiles,1);
    shipSize = zeros(nFiles,1);
    draught = zeros(nFiles,1);
    for iFile = 1:nFiles
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
            1,(hdr.xhd.byte_length/hdr.samp.byte));
        % get associated info from text file
        textData = importdata(txtFile);
        k1Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'ShipType'))==1);
        if ~isempty(k1Idx)
            [k1,~]= regexp(textData.textdata{k1Idx,1},'ShipType=(\w*)','tokens','match');
            shipType{iFile,1} = k1{1,1};
        end
        k2Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'IMO'))==1);
        if ~isempty(k2Idx)
            [k2,~]= regexp(textData.textdata{k2Idx,1},'IMO=(\d*)','tokens','match');
            IMO(iFile,1) = str2num(char(k2{1,1}));
        end
        k3Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'toBow'))==1);
        if ~isempty(k3Idx)
            [k3,~]= regexp(textData.textdata{k3Idx,1},'toBow\[m\]=(\d*.\d*)','tokens','match');
            shipSize(iFile,1) = str2num(char(k3{1,1}));
        end
        k4Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'Draught'))==1);
        if ~isempty(k4Idx)
            [k4,~]= regexp(textData.textdata{k4Idx,1},'Draught\[m\]=(\d*\.\d*)','tokens','match');
            draught(iFile,1) = str2num(char(k4{1,1}));
        end
        
        [specMat,f] = makeSpectrogram(wavData);
        specMatTruncHF = specMat(1:1600,:);
        F = griddedInterpolant(specMatTruncHF);
        [sx,sy,sz] = size(specMatTruncHF);
        log10sx = log10(sx);
        log10sxVec = (0:(log10sx/1024):log10sx);
        log10xq = 10.^(log10sxVec(2:end));
        fLog10 = interp1(f,log10xq);
        %     logsx = log(sx);
        %     logsxVec = (1:(logsx/1024):logsx);
        %     logxq = exp(logsxVec(2:end))';
        
        yq = (0:sy/1024:sy)';
%         if size(yq,1)==1023
%             yq = (.5:sy/1024:sy)';
%         end
        %xq = (1:sx/1024:sx)';
        log10vq = F({log10xq(:,:),yq});
        imageStack(:,:,iFile) = log10vq;
        %     logvq = F({logxq(:,:),yq});
        % 	vq = F({xq,yq});
    end
    
    % prune out empty IMO, which seems to mean no auxiliary info
    keepers = IMO~=0;
    imageStack = imageStack(:,:,keepers);
    shipType = shipType(keepers);
    IMO = IMO(keepers);
    shipSize = shipSize(keepers);
    draught = draught(keepers);
    
    imageStackAll = [imageStackAll,imageStack];
    shipTypeAll = [shipTypeAll;shipType];
    IMOAll = [IMOAll;IMO];
    shipSizeAll = [shipSizeAll;shipSize];
    draughtAll = [draughtAll;draught];
    
end
toc


function [sdB,f] = makeSpectrogram(data)

overlap = 50;
nfft = 3750;
noverlap = (overlap/100)*nfft;
fs = 10e3;

% this seems to match the plot made by spectrogram with y-axis option
[~,f,t,psd] = spectrogram(data,hanning(nfft),noverlap,nfft,fs,'psd');
sdB = 10*log10(psd);
end
