
winterSet = load('F:\ShippingCINMS_data\COP_monthStack_2015-01.mat');
myWinterType = [winterSet.subSetData(:).shipType]';
figure(2)
subplot(2,2,1)
imagesc(mean(winterSet.imageStack(:,:,find(strcmp(myWinterType,'Cargo'))),3))
set(gca,'YDir','normal')
%colorbar
caxis([-50,-5])
figure(3)
subplot(2,2,1)
imagesc(log(mean(10.^winterSet.imageStack(:,:,find(strcmp(myWinterType,'Cargo'))),3)))
set(gca,'YDir','normal')
%colorbar
caxis([-80,80])
colormap(jet)


summerSet = load('F:\ShippingCINMS_data\COP_monthStack_2014-08.mat');
mySummerType = [summerSet.subSetData(:).shipType]';
figure(2)
subplot(2,2,2)
imagesc(mean(summerSet.imageStack(:,:,find(strcmp(mySummerType,'Cargo'))),3))
set(gca,'YDir','normal')
%colorbar
caxis([-50,-5])
figure(3)
subplot(2,2,2)
imagesc(log(mean(10.^summerSet.imageStack(:,:,find(strcmp(mySummerType,'Cargo'))),3)))
set(gca,'YDir','normal')
%colorbar
caxis([-80,80])
colormap(jet)

winterSet2016 = load('F:\ShippingCINMS_data\COP_monthStack_2016-01.mat');
myWinterType2016 = [winterSet2016.subSetData(:).shipType]';
figure(2)
subplot(2,2,3)
imagesc(mean(winterSet2016.imageStack(:,:,find(strcmp(myWinterType2016,'Cargo'))),3))
set(gca,'YDir','normal')
%colorbar
caxis([-50,-5])
figure(3)
subplot(2,2,3)
imagesc(log(mean(10.^winterSet2016.imageStack(:,:,find(strcmp(myWinterType2016,'Cargo'))),3)))
set(gca,'YDir','normal')
%colorbar
caxis([-80,80])
colormap(jet)

summerSet2015 = load('F:\ShippingCINMS_data\COP_monthStack_2015-08.mat');
mySummerType2015 = [summerSet2015.subSetData(:).shipType]';
figure(2)
subplot(2,2,4)
imagesc(mean(summerSet2015.imageStack(:,:,find(strcmp(mySummerType2015,'Cargo'))),3))
set(gca,'YDir','normal')
%colorbar
caxis([-50,-5])
colormap(jet)
set(gca,'Ytick',[1,492,822],'YTickLabel',[10,100,1000])

figure(3)
subplot(2,2,4)
flog10 = summerSet2015.subSetData(1).fLog10;
imagesc(log(mean(10.^summerSet2015.imageStack(:,:,find(strcmp(mySummerType2015,'Cargo'))),3)))
set(gca,'YDir','normal')
%colorbar
caxis([-80,80])
colormap(jet)
set(gca,'Ytick',[1,492,822],'YTickLabel',[10,100,1000])