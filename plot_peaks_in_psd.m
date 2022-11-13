function plot_peaks_in_psd(myPSD,f)
myPeaks = [];
myLocs = {};
for I1=1:size(myPSD,2)
    %[pks,locs] = findpeaks(myPSD(:,I1)-65,'MinPeakHeight',10);
    [pks,locs] = findpeaks(myPSD(:,I1)-median(myPSD,'all'),'MinPeakHeight',prctile(myPSD,95,'all')-median(myPSD,'all'));

    myPeaks{I1} = pks;
    myLocs{I1} = locs;
end
figure(9);
clf
peakMat = zeros(length(f),size(myPSD,2));
for iP = 1:size(myPeaks,2)
    plot(ones(size(myLocs{iP}))*iP,f(myLocs{iP}),'.k','markersize',4)
    hold on
end



