clearvars

addpath('E:\Code\SPICE-box\SPICE-Detector\io')
addpath('E:\Code\SPICE-box\SPICE-Detector\funs')
tfDir = 'E:\TFs'; % folder containing transfer functions
outDir = 'H:\ShippingCINMS_data';
folderTag = 'COP';
mainDir = fullfile(outDir,folderTag);
dirList = dir(fullfile(mainDir,'2*'));

% get list of which tfs go with which deployments.
tfList = importdata('H:\ShippingCINMS_data\CINMS_TFs.csv');

% load(txtFile)
% load(wavFile)
% Bad data ranges:
badDateRanges = [2018-02-16,2018-07-11;
    2015-06-11,	2015-09-01;
    2016-11-09,	2017-02-22];


for iDir = 1:length(dirList)
    
    subDir = fullfile(dirList(iDir).folder,dirList(iDir).name);
    fList = dir(fullfile(subDir,'*.wav'));
    nFiles = size(fList,1);
    
    
    p.DateRegExp = '_(\d{6})_(\d{6})';
    for iFile = 1:nFiles
        soundFile = fullfile(fList(iFile).folder,fList(iFile).name);
        % check if text file exists
        txtFile = strrep(soundFile,'.wav','.txt');
        
        if ~exist(txtFile,'file')
            warning('Could not find file %s, skipping.','txtFile')
            continue
        end
        
        hdr = io_readWavHeader(soundFile,p.DateRegExp);
        wavData = io_readWav(soundFile,hdr,...
            0,(hdr.end.dnum-hdr.start.dnum)*24*60*60,...
            'Units','s','Normalize','unscaled');
        
        % get associated info from text file
        textData = importdata(txtFile);
        
        [siteName,~] = regexp(textData.textdata{1,1},'HARPSite=(\w*)','tokens','match');
        siteName = siteName{1};
        
        k1Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'HARPLat'))==1);
        if ~isempty(k1Idx)
            [k1,~]= regexp(textData.textdata{k1Idx,1},'HARPLat=(\d*\.\d*)','tokens','match');
            HARPLat = str2double(cell2mat(k1{1,1}));
        end
        k2Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'HARPLon'))==1);
        if ~isempty(k2Idx)
            [k2,~]= regexp(textData.textdata{k2Idx,1},'HARPLon=(-\d*\.\d*)','tokens','match');
            HARPLon = str2double(cell2mat(k2{1,1}));
        end
        
        k4Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'CPATime'))==1);
        if ~isempty(k4Idx)
            [k4,~]= regexp(textData.textdata{k4Idx,1},'CPATime\[UTC\]=(.*)','tokens','match');
            CPATime = datenum(char(k4{1,1}));
        end
        
        k5Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'CPADistance'))==1);
        if ~isempty(k5Idx)
            [k5,~]= regexp(textData.textdata{k5Idx,1},'CPADistance\[m\]=(\d*)','tokens','match');
            CPADist = str2num(char(k5{1,1}));
        end
        
        k6Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'UTC'))==1);
        if ~isempty(k6Idx)
            timeSteps = datenum(textData.textdata(k6Idx(end)+1:end,1));
        end
        
        % get TF
        tfIdx = find(~cellfun(@isempty,strfind(tfList.textdata(:,1),siteName)));
        tfNum = tfList.data(tfIdx-1);
        tfFolder = dir(fullfile(tfDir,[num2str(tfNum),'*']));
        tfFile = dir(fullfile(tfFolder.folder,tfFolder.name,'*.tf'));
        
        if isempty(tfFile)
            error('missing tf file')
        end
        
        %         B = HARPLat;r1 = 6378.137;r2 = 6371.001;
        %         R = sqrt([(r1^2 * cos(B))^2 + (r2^2 * sin(B))^2 ] / [(r1 * cos(B))^2 + (r2 * sin(B))^2]); % radius of earth at HARP lat
        %         distH2Sdeg = sqrt((HARPLat-textData.data(:,1)).^2+(HARPLon-textData.data(:,2)).^2);
        %         distH2Skm = deg2km(distH2Sdeg,R);
        %
        [xRange,yRange] = latlon2xy(HARPLat,HARPLon,textData.data(:,1),textData.data(:,2));
        range1  = sqrt(xRange.^2+yRange.^2);
        %         figure(2);clf
        %         plot(timeSteps,abs(range1/1000),'*')
        %         hold on
        %         plot(timeSteps,distH2Skm,'*r')
        %
        % plot(timeSteps,ones(size(xyRanges))*CPADist/1000,'-k')
        % datetick
        
        
        % get times from textData.textdata
        % approach
        [~,cpaIdx] = min(abs(timeSteps-CPATime));
        myDists = (6:-.01:4)*1000; % make a vector of distances bin to sample at
        timesToSample = interp1(range1(1:cpaIdx),timeSteps(1:cpaIdx),myDists);
        myDistSpec = nan(length(myDists),5001);
        myDistSpecImag = [];
        uppc = [];
        for iDist = 1:length(myDists)
            
            myTimeIdx = round(hdr.fs*((timesToSample(iDist)-hdr.start.dnum)*60*60*24));
            if isnan(myTimeIdx) || myTimeIdx<1
                continue
            end
            myData = wavData(max(myTimeIdx-5000,1):min(myTimeIdx+5000-1,length(wavData)));
            if length(myData)<10000
                myData = [myData;zeros(10000-length(myData),1)];
            end
            [~,f,t,psd] = spectrogram(myData,hanning(10000),0,10000,hdr.fs,'psd');
            if isempty(uppc)&& ~isempty(f)
                [~, uppc] = fn_tfMap(fullfile(tfFile.folder,tfFile.name),f);
                
            end
            sdB = 10*log10(psd);
            if ~isempty(sdB)
                myDistSpec(iDist,:) = (sdB+uppc)';
            end
        end
        finalDistSpec = max(myDistSpec(:,5:4000),40);

        % departure
        [~,cpaIdx] = min(abs(timeSteps-CPATime));
        myDistsD = (4:.01:6)*1000;
        timesToSampleD = interp1(range1(cpaIdx+1:end),timeSteps(cpaIdx+1:end),myDistsD);
        myDistSpecD = nan(length(myDistsD),5001);
        uppc = [];
        for iDist = 1:length(myDistsD)
            
            myTimeIdx = round(hdr.fs*((timesToSampleD(iDist)-hdr.start.dnum)*60*60*24));
            if isnan(myTimeIdx) || myTimeIdx<1
                continue
            end
            myData = wavData(max(myTimeIdx-5000,1):min(myTimeIdx+5000-1,length(wavData)));
            if length(myData)<10000
                myData = [myData;zeros(10000-length(myData),1)];
            end
            [~,f,t,psd] = spectrogram(myData,hanning(10000),0,10000,hdr.fs,'psd');
            if isempty(uppc)&& ~isempty(f)
                [~, uppc] = fn_tfMap(fullfile(tfFile.folder,tfFile.name),f);
                
            end
            sdB = 10*log10(psd);
            if ~isempty(sdB)
                myDistSpecD(iDist,:) = (sdB+uppc)';
            end
            
            
        end
        finalDistSpecD = max(myDistSpecD(:,5:4000),40);
        figure(1)
        imagesc([finalDistSpec;finalDistSpecD]');set(gca,'ydir','normal');
        figure(2);spectrogram(wavData,1000,0,1000,hdr.fs,'psd');
        colormap(jet);
    end
end


