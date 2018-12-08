% starter script for project 3
DO_TOY = true;
DO_BLEND = false;
DO_MIXED  = false;
DO_COLOR2GRAY = false;

if DO_TOY 
    toyim = im2double(imread('./toy_problem.png')); 
    % im_out should be approximately the same as toyim
    im_out = toy_reconstruct(toyim);
    disp(['Error: ' num2str(sqrt(sum(toyim(:)-im_out(:))))])
end

if DO_BLEND
    im_background = imresize(im2double(imread('./samples/im2.jpg')), 0.5, 'bilinear');
    im_object = imresize(im2double(imread('./samples/penguin-chick.jpeg')), 0.5, 'bilinear');

    % get source region mask from the user
    objmask = getMask(im_object);
    % align im_s and mask_s with im_background
    [im_s, mask_s] = alignSource(im_object, objmask, im_background);

    % blend
    im_blend = poissonBlend(im_s, mask_s, im_background);
    figure(3), hold off, imshow(im_blend)
end

if DO_MIXED
    % read images
    %...
    
    % blend
    im_blend = mixedBlend(im_s, mask_s, im_bg);
    figure(3), hold off, imshow(im_blend);
end

if DO_COLOR2GRAY
    im_rgb = im2double(imread('./samples/colorBlindTest35.png'));
    im_gr = color2gray(im_rgb);
    figure(4), hold off, imagesc(im_gr), axis image, colormap gray
end



function v = toy_reconstruct(im)
 
[imh, imw, nb] = size(im);
im2var = zeros(imh, imw); 
im2var(1:imh*imw) = 1:imh*imw;

e = 0

for y = 1:imh
    for x=1:imw-1
        e=e+1; 
        A(e, im2var(y,x+1))=1; 
        A(e, im2var(y,x))=-1; 
        b(e) = im(y,x+1)-im(y,x);
    end
end

for y = 1:imh-1
    for x = 1:imw
        e=e+1;
        A(e, im2var(y+1,x))=1;
        A(e, im2var(y,x))=-1;
        b(e) = im(y+1,x)-im(y,x);
    end
end

e=e+1;
A(e, im2var(1,1))=1;
b(e)=im(1,1);

v = A\b;

end

