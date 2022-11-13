imagesc(thisPassage)
set(gca,'ydir','normal')

imagesc(max(thisPassage,65))
set(gca,'ydir','normal')

plot(thisPassage(200,:))
myPeaks = {};
myLocs = {};
for I1=1:512/2
    [pks,locs] = findpeaks(thisPassage(:,0+I1)-65,'MinPeakHeight',15);
    myPeaks{I1} = pks;
    myLocs{I1} = locs;
end

figure(9);%clf
for iP = 1:size(myPeaks,2)
    plot(ones(size(myLocs{iP}))*thisDistVec(iP),...
        myLocs{iP},'.r')
    hold on
end

figure(10);clf
hist(diff(vertcat(myLocs{:})),1:30)
xlim([1,20])

plot(median(thisPassage(:,240:272),2))

POVDat


