inDir = 'M:\ShipNoise_nnet_input';
fList = dir(fullfile(inDir,'*.mat'));
myDate = [];
for iD=1:length(fList)
   myDate(iD,1) =  datenum(fList(iD).name(11:end-4),'yymmddHHMMSS');
end
[C,IX] = sort(myDate);
fListSort = fList(IX);
%%

for iF=100:150
    load(fullfile(inDir, fListSort(iF).name))
    myPeaks = {};
    myLocs = {};
    for I1=1:512
        [pks,locs] = findpeaks(thisPassage(:,0+I1)-65,'MinPeakHeight',5);
        myPeaks{I1} = pks;
        myLocs{I1} = locs;
    end
    figure(9);
    clf
    subplot(1,3,1)
    imagesc(1:512,1:300,thisPassage)
    set(gca,'ydir','normal')
    %colorbar
    set(gca,'clim',[50,85])
    ylabel('Frequency (Hz)')
   subplot(1,3,2)
    myFreq = 1:(300/(512+1)):300;
    peakMat = zeros(512,512);
    for iP = 1:size(myPeaks,2)
        plot(ones(size(myLocs{iP}))*thisDistVec(iP),myFreq(myLocs{iP}),'.k','markersize',4)
        hold on
        myInds = sub2ind(size(peakMat),myLocs{iP},(ones(size(myLocs{iP}))*iP));
        peakMat(myInds) =  thisPassage(myInds);
    end
    %xlim([0,512])
    subplot(1,3,3)
    imagesc(peakMat);set(gca,'ydir','normal');
end

