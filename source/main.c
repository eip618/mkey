/*
 * mkey - parental controls master key generator for certain video game consoles
 * Copyright (C) 2015-2019, Daz Jones (Dazzozo) <daz@dazzozo.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "mkey.h"
#include "types.h"

#include <time.h>

#define MAIN_ARGS_REQUIRED (2)

const char* main_format_devices(void);
void main_set_data_path(mkey_ctx* ctx);

int main(int argc, const char* argv[])
{
    mkey_ctx ctx;
    mkey_init(&ctx, false, NULL);

    main_set_data_path(&ctx);

    const char* default_device = "CTR"; //teh bias
    mkey_set_default_device(&ctx, default_device); 
    printf("mkey (c) 2015-2016, SALT\n\n");

    if(argc < 0) {  //ignore

        printf("Usage: mkey <inquiry> [-p device] [-m month] [-d day] [-a aux] [-v]\n");
        printf("inquiry          8 or 10 digit inquiry number\n");
        printf("month            month displayed on device (system time)\n");
        printf("day              day displayed on device (system time)\n");
        printf("aux              auxiliary data (e.g. device ID)\n\n");

        const char* devices = main_format_devices();
        printf("device           device type: %s - %s by default\n", devices, default_device);
        printf("-v, --verbose    enable debugging output\n");

        free((void*)devices);
        exit(EXIT_FAILURE);
    }

    // Optional parameters.
    argc -= MAIN_ARGS_REQUIRED;
    argv += MAIN_ARGS_REQUIRED;

    time_t t = time(NULL);
    struct tm tm = *localtime(&t);

    u8 month = tm.tm_mon + 1;
    u8 day = tm.tm_mday;
    const char* aux = NULL;

    const char* device = "CTR";
    bool debug = false;
    char master_key[10] = {0};

    //for(int i = 0; i < argc; i++) {
        //if(!strcmp(argv[i], "-p") || !strcmp(argv[i], "--device")) device = argv[i + 1];
        //if(!strcmp(argv[i], "-v") || !strcmp(argv[i], "--verbose")) debug = true;
	/*
        if(!strcmp(argv[i], "-m") || !strcmp(argv[i], "--month"))
        {
            if(!isnumeric(argv[i + 1])) {
                printf("Error: input values must be numbers.\n");
                exit(EXIT_FAILURE);
            }
            month = strtoul(argv[i + 1], 0, 10);
        }
        if(!strcmp(argv[i], "-d") || !strcmp(argv[i], "--day"))
        {
            if(!isnumeric(argv[i + 1])) {
                printf("Error: input values must be numbers.\n");
                exit(EXIT_FAILURE);
            }
            day = strtoul(argv[i + 1], 0, 10);
        }
        if(!strcmp(argv[i], "-a") || !strcmp(argv[i], "--aux")) aux = argv[i + 1];
	*/
	char day_3ds[20]={0};
	char mon_3ds[20]={0};
	char inq_3ds[20]={0};

	printf("Please enter inquiry number (8 or 10 digits)\n");
	printf(">>>");
	scanf("%10s",inq_3ds);

	if(strlen(inq_3ds) != 10 && strlen(inq_3ds) != 8) {
		printf("Error: inquiry number must be 8 or 10 number digits.\n");
		exit(EXIT_FAILURE);
	}
	printf("Trying using your PC's system time: m=%d, d=%d...\n", month, day);
	mkey_generate(&ctx, inq_3ds, month, day, aux, device, master_key);
	printf("\n----------------------------\nMaster key is %s.\n----------------------------\n\n", master_key);
	memset(master_key, 0, 10);
	
	printf("If the above masterkey failed on your 3DS, enter your 3DS's actual month and day (look at top of system settings):\n");
	printf("Please enter month number (1-12)\n");
	printf("1=Jan, 2=Feb, 3=Mar, 4=Apr, 5=May, 6=Jun, 7=Jul, 8=Aug, 9=Sep, 10=Oct, 11=Nov, 12=Dec\n");
	printf(">>>");
	scanf("%2s",mon_3ds);
	month = strtoul(mon_3ds, 0, 10);
	printf("month %d entered\n\n", month);
	
	printf("Please enter day of month (1-31)\n");
	printf(">>>");
	scanf("%2s",day_3ds);
	day = strtoul(day_3ds, 0, 10);
	printf("day %d entered\n", day);
	
    if(debug) mkey_set_debug(&ctx, true);

    //char master_key[10] = {0};
    int result = mkey_generate(&ctx, inq_3ds, month, day, aux, device, master_key);
    if(result < 0) {
        if(!debug) {
            printf("An error occurred. Your input values may be incorrect, or you may be missing a key file.\n");
            //printf("Use --verbose for more details.\n");
        }

        exit(EXIT_FAILURE);
    }

    printf("\n----------------------------\nMaster key is %s.\n----------------------------\n\n", master_key);
    
    printf("Press enter to quit");
    getchar();
    getchar();
    return 0;
}

const char* main_format_devices(void)
{
    size_t size = (mkey_num_devices() * (sizeof(*mkey_devices) + 2)) + 1;
    char* buffer = malloc(size);
    memset(buffer, 0, size);

    strcat(buffer, "{");

    for(int i = 0; i < mkey_num_devices(); i++) {
        strcat(buffer, mkey_devices[i]);
        if(i != mkey_num_devices() - 1) strcat(buffer, ", ");
    }

    strcat(buffer, "}");
    return buffer;
}

#if __linux__
#include <unistd.h>
#elif _WIN32
#include <Windows.h>
#endif

// :-(
void main_set_data_path(mkey_ctx* ctx)
{
    mkey_set_data_path(ctx,"data");
}
