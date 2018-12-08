im_background = imresize(im2double(imread('./imgs/prague.jpg')), 1, 'bilinear');
im_object = imresize(im2double(imread('./imgs/boat.jpg')), 1, 'bilinear');
% get source region mask from the user
objmask = getMask(im_object);
% align im_s and mask_s with im_background
[im_s, mask_s] = alignSource(im_object, objmask, im_background);
% save images to the disk. 
imwrite(im_s, './imgs/boat_aligned.png'); 
imwrite(mask_s, './imgs/boat_mask.png');
