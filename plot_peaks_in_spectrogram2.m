inDir = 'M:\ShipNoise_nnet_input';
fList = dir(fullfile(inDir,'*.mat'));

for iF=1:10
    load(fullfile(inDir, fList(iF).name))
myPeaks = {};
myLocs = {};
for I1=1:512
[pks,locs] = findpeaks(thisPassage(:,0+I1)-65,'MinPeakHeight',5);
myPeaks{I1} = pks;
myLocs{I1} = locs;
end
figure(9);clf
subplot(1,2,1)
imagesc(1:512,1:300,thisPassage)
set(gca,'ydir','normal')
%colorbar
set(gca,'clim',[50,85])
ylabel('Frequency (Hz)') 
subplot(1,2,2)
myFreq = 1:(300/(512+1)):300;
for iP = 256:size(myPeaks,2)
plot(ones(size(myLocs{iP}))*thisDistVec(iP),myFreq(myLocs{iP}),'.k','markersize',4)
hold on
end
%xlim([0,512])

end