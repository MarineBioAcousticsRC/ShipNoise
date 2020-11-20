clearvars

addpath('E:\Code\Triton\Remoras\SPICE-Detector\io')
% functions to the shipParsing directory.
% addpath('E:\Code\SPICE-box\SPICE-Detector\funs')
tfDir = 'R:\Shared drives\MBARC_TF'; % folder containing transfer functions
outDir = 'F:\ShippingCINMS_data\'; % where the files will save. I didn't replicate
% the folder structure, not sure what makes sense for you but happy to
% change as needed.
folderTag = 'COP';
mainDir = fullfile(outDir,folderTag);
dirList = dir(fullfile(mainDir,'2*'));
plotOn = 1; % 1 for plots, 0 for no plots
saveDir = 'F:\ShippingCINMS_data\rangeFreqSpectrograms_COP_ALL';
if ~isfolder(saveDir)
    mkdir(saveDir)
end
% get list of which tfs go with which deployments.
tfList = importdata('F:\ShippingCINMS_data\CINMS_TFs.csv');

% load(txtFile)
% load(wavFile)
% Bad data ranges:
badDateRanges = [2018-02-16,2018-07-11;
    2015-06-11,	2015-09-01;
    2016-11-09,	2017-02-22];

% Frequency limits used to prune the spectrograms.
minFreq = 10;% in Hz
maxFreq = 3000;% inHz
dataLength = 10000; % amount of data to grab in samples for each range step.
nfft = 10000; % Bin size = fs/nfft = 10000/10

% Vector of distances to sample at. If you have too many passages with
% bands of no data, this can be adjusted to fix that. For instance, maybe
% vessels don't come closer than 4.5 km, so you're always getting empty
% values for close ranges. In that case, increase 4 to 4.5.
minRange = 4;
maxRange = 5;
rangeStep = .02;
myDistsApproach = (maxRange:-rangeStep:minRange)*1000; % ends up being in meters
myDistsDepart = (minRange:rangeStep:maxRange)*1000;
myDists = [myDistsApproach,myDistsDepart];
goodSet = readtable('F:\ShippingCINMS_data\forKait_data2014_2018_noStrum_1Hour_Cargo.csv', 'Delimiter',',');
for iDir = 8:length(dirList)
    
    subDir = fullfile(dirList(iDir).folder,dirList(iDir).name);
    fList = dir(fullfile(subDir,'*.wav'));
    nFiles = size(fList,1);
    fileDate = [];
    for iD = 1:nFiles
        fileDate(iD,1) = datenum(fList(iD).name(end-16:end-4),'yymmdd_HHMMSS');
    end
    [X,IX] = sort(fileDate);
    psdStack = [];
    rangeStack = [];
    interpedTimeStack = [];
    shipSizeStack = [];
    draughtStack = [];
    IMOStack = [];
    shipTypeStack = {};
    CPADistStack = [];
    CPATimeStack = [];
    meanSOGStack = [];
    MMSIStack = [];
    
    
    p.DateRegExp = '_(\d{6})_(\d{6})';
    n = 1;
    usedFList =[];
    for iFile = 1:nFiles
        %         if isempty(find(strcmp(char(fList(IX(iFile)).name),table2cell(goodSet))))
        %             disp('Not in VZ set')
        %             continue
        %         end
        if intersect(usedFList,IX(iFile))
            disp('file is 2nd half of a pair, skipping')
            continue
        end
        soundFile = fullfile(fList(IX(iFile)).folder,fList(IX(iFile)).name);
        % check if text file exists
        txtFile = strrep(soundFile,'.wav','.txt');
        matchingFilesAll = find(strncmp(fList(IX(iFile)).name,cellstr(vertcat(fList(:).name)),16));
        matchingFile = setdiff(matchingFilesAll,IX(iFile));
        
        mergeWave = 0;
        if ~isempty(matchingFile)&& length(matchingFile)==1
            % warning, assumes only one file will match, never more.
            time1 = datenum(fList(IX(iFile)).name(end-16:end-4),'yymmdd_HHMMSS');
            
            time2 = datenum(fList(matchingFile).name(end-16:end-4),'yymmdd_HHMMSS');
            if time2>time1 && (time2-time1)<datenum([0,0,0,0,38,0])
                disp('found second wav file following this one')
                mergeWave = 1;
                soundFile2 = fullfile(fList(matchingFile).folder,fList(matchingFile).name);
                txtFile2 = strrep(soundFile2,'.wav','.txt');
                usedFList = [usedFList;matchingFile];
            end
            
        elseif length(matchingFile)>1
            usedFList = [usedFList;matchingFile];
        end
        if ~exist(txtFile,'file')
            if mergeWave && exist(txtFile2,'file')
                txtFile = txtFile2;
                disp('Using text file from 2nd half')
            else
                warning('Could not find file %s, skipping.','txtFile')
                continue
            end
        end
        try
            hdr = sp_io_readWavHeader(soundFile,p.DateRegExp);% this just reads the wav file header info
            if mergeWave
                hdr2 = sp_io_readWavHeader(soundFile2,p.DateRegExp);
            end
        catch
            mergeWave = 0;
            continue
        end
        % wav file sample rate, other basic info, and interprets
        % the start time from the file name. You probably have a python
        % script that would do this.
        if sum(hdr.start.dnum>=badDateRanges(:,1) & hdr.start.dnum<=badDateRanges(:,2))
            disp('Event falls within bad date range. Skipping.\n')
            mergeWave = 0;
            continue
        end
        fID = fopen(soundFile);
        
        
        wavData = sp_io_readWav(fID,hdr,...
            0,(hdr.end.dnum-hdr.start.dnum)*24*60*60,...
            'Units','s','Normalize','unscaled');
        fclose(fID);
        if mergeWave
            fID = fopen(soundFile2);
            
            
            wavData2 = sp_io_readWav(fID,hdr2,...
                0,(hdr2.end.dnum-hdr2.start.dnum)*24*60*60,...
                'Units','s','Normalize','unscaled');
            wavData = [wavData;wavData2];
            fclose(fID);

        end
        
        mergeWave = 0; % done merging, so reset it before we forget.
        
        % get info from text file to be able to calculate range.
        textData = importdata(txtFile);
        if ~isfield(textData,'textdata')
            disp('Unexpected format of imported text data. Skipping.')
            continue
        end
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
        k1Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'ShipType'))==1);
        shipType = [];
        if ~isempty(k1Idx)
            [k1,~]= regexp(textData.textdata{k1Idx,1},'ShipType=(\w*)','tokens','match');
            shipType = k1{1,1};
        end
        k2Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'IMO='))==1);
        IMO = [];
        if ~isempty(k2Idx)
            k2Idx = k2Idx(1);% hit a case with 2 IMO#s ??
            [k2,~]= regexp(textData.textdata{k2Idx,1},'IMO=(\d*)','tokens','match');
            IMO = str2double(char(k2{1,1}));
        end
        if isempty(IMO)
            disp('no IMO.')
            continue
        end
        
        k3Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'toBow'))==1);
        shipSize = [];
        if ~isempty(k3Idx)
            [k3,~]= regexp(textData.textdata{k3Idx,1},'toBow\[m\]=(\d*.\d*)','tokens','match');
            shipSize = str2num(char(k3{1,1}));
        end
        k4Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'Draught'))==1);
        
        draught = [];
        if ~isempty(k4Idx)
            [k4,~]= regexp(textData.textdata{k4Idx,1},'Draught\[m\]=(\d*\.\d*)','tokens','match');
            draught = str2num(char(k4{1,1}));
        end
        
        k7Idx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'MMSI='))==1);
        if ~isempty(k7Idx)
            [k7,~]= regexp(textData.textdata{k7Idx,1},'MMSI=(\d*)','tokens','match');
            MMSI = str2double(k7{1,1});
        end
        if isfield(textData,'data') && size(textData.data,2)>3
            meanSOG = mean(textData.data(:,4));
        end
        
        % get TF
        tfIdx = find(~cellfun(@isempty,strfind(tfList.textdata(:,1),siteName)));
        tfNum = tfList.data(tfIdx-1);
        [tfFolder, TFName] = pick_TF_subdirs(tfNum,tfDir);
        
        %tfFolder = dir(fullfile(tfDir,[num2str(tfNum),'*']));
        tfFile = fullfile(tfFolder,TFName.name); % dir(fullfile(tfFolder.folder,tfFolder.name,'*.tf'));
        
        if isempty(tfFile)
            error('missing tf file')
        end
        
        
        [xRange,yRange] = latlon2xy(HARPLat,HARPLon,textData.data(:,1),textData.data(:,2));
        range1  = sqrt(xRange.^2+yRange.^2);
        [timeSteps,ia,ic] = unique(timeSteps,'stable');
        range1 = range1(ia);
        
        [s,f,t,ps] = spectrogram(wavData,nfft,0,1:1:1000,hdr.fs,'psd'); % sanity check to compare time freq vs range freq.
        [~, uppc] = fn_tfMap(tfFile,f);
        myPSD = 10*log10(ps) + uppc;
        
        
        interpedTime = min(timeSteps):(1/(24*60)):max(timeSteps);
        interpedRange = interp1(timeSteps,range1,hdr.start.dnum+(t/(60*24*60)));
        if sum(~isnan(interpedRange))==0
            continue
        end
        
        interpedRange = (smooth(interpedRange,30,'rloess')');
        [~,cpaIdx] = min(interpedRange);
        
        myRange = max(1,(cpaIdx-400)):min(length(interpedRange),(cpaIdx+400));
        
        % figure(2);clf
        % plot(timeSteps,abs(range1/1000),'*')
        % hold on
        % plot(timeSteps,distH2Skm,'*r')
        %
        % plot(timeSteps,ones(size(xyRanges))*CPADist/1000,'-k')
        % datetick

        % get times from textData.textdata
        % approach
        
        if 1
            figure(1);clf
            
            subplot(1,2,1)
            
            imagesc(hdr.start.dnum+(t/(60*24*60)),f(1:300),myPSD(1:300,:))
            set(gca,'yDir','normal','clim',[30,100])
            hold on
            plot([hdr.start.dnum+(t(myRange(1))/(60*24*60)),hdr.start.dnum+(t(myRange(1))/(60*24*60))],[0,300],'--k')
            plot([hdr.start.dnum+(t(myRange(end))/(60*24*60)),hdr.start.dnum+(t(myRange(end))/(60*24*60))],[0,300],'--k')
            
            hold off
            colorbar
            colormap(jet);
            title('Time-Frequency')
            datetick('x','keepTicks','keepLimits')
            sub1Xlims = get(gca,'xlim');
            subplot(1,2,2)
            plot(hdr.start.dnum+(t/(60*24*60)),interpedRange,'linewidth',2);
            hold on
            plot([hdr.start.dnum+(t(myRange(1))/(60*24*60)),hdr.start.dnum+(t(myRange(1))/(60*24*60))],[min(interpedRange),max(interpedRange)],'--k')
            plot([hdr.start.dnum+(t(myRange(end))/(60*24*60)),hdr.start.dnum+(t(myRange(end))/(60*24*60))],[min(interpedRange),max(interpedRange)],'--k')
            
            hold off
            xlabel('Time')
            ylabel('Horizontal Range (km)')
            title(sprintf('Transit: %s',datestr(hdr.start.dnum)))
            datetick('x','keepTicks','keepLimits')
            xlim(sub1Xlims)
            1;
        end
        
        if length(myRange)<801
            disp('too short, skipping.')
            continue
        end

        [~,nameStem,~] = fileparts(soundFile);
        %keepTF = [];
        %         keepTF = input('Save passage?  Y/N [Y]:','s');
        %         if  isempty(keepTF) || strcmpi(keepTF,'y')
        outFileName = [nameStem,'_timeFreq1000pts.mat'];
        % output file in netcdf format
        save(fullfile(saveDir,outFileName),'f','interpedRange','myPSD','shipSize','draught','IMO','shipType',...
            'CPADist','CPATime','meanSOG','shipSize','interpedTime','MMSI','-v7.3')
        psdStack(:,:,n) = myPSD(:,myRange);
        
        interpedTimeStack(n,:) = t(myRange) ;
        rangeStack(n,:) = interpedRange(:,myRange);
        shipSizeStack(n,1) = shipSize;
        draughtStack(n,:) = draught;
        IMOStack(n,:) = IMO;
        shipTypeStack(n) = shipType;
        CPADistStack(n,:) = CPADist;
        CPATimeStack(n,:) = CPATime;
        meanSOGStack(n,:) = meanSOG;
        MMSIStack(n,:) =MMSI;
        fprintf('Done with file %0.0f of %0.0f\n', iFile, nFiles)
        n = n+1;
        saveas(gcf,strrep(fullfile(saveDir,outFileName),'.mat','.fig'))
        saveas(gcf,strrep(fullfile(saveDir,outFileName),'.mat','.png'))
    end
    fprintf('Done with folder %0.0f of %0.0f\n', iDir, length(dirList))
    save(fullfile(saveDir,[dirList(iDir).name,'_timeFreqStack.mat']),...
        'psdStack','rangeStack','shipSizeStack','draughtStack','IMOStack',...
        'shipTypeStack','CPADistStack','CPATimeStack','meanSOGStack','MMSIStack')
    %         else
    %             disp('rejected by user')
    %         end
    
    
end
