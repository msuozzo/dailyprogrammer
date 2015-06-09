#include <iostream>
#include <fstream>
#include <regex>
#include <numeric>
#include <functional>
#include <vector>


using namespace std;

/**
 * Return a closure around `join_str` which joins two string parameters.
 */
function<string (const string, const string)> join(const string join_str) {
    return [&](string acc, const string next) { return acc + join_str + next; };
}

/**
 * Iterate through the file `play_file` and search for the dialog passage
 * containing the quote `search_string`
 *
 * Return an empty string on failure
 */
string find_dialog_passage(ifstream& play_file, const string& search_string) {
    regex search_pat("^.*" + search_string + ".*$");
    regex dialog_pat(R"(^ {4}(.+)$)");
    smatch matches;
    vector<string> block{};
    bool found_match = false;
    for (string line; getline(play_file, line); ) {
        if (regex_search(line, matches, dialog_pat)) {
            block.push_back(matches[1]);
            found_match = (!found_match) ? regex_match(line, search_pat) : found_match;
        } else if (!found_match) {
            block.clear();
        } else {
            break;
        }
    }
    if (found_match) {
        return accumulate(block.begin() + 1, block.end(), block[0], join("\n"));
    }
    return string();
}

int main(int argc, char **argv) {
    if (argc < 3) {
        cout << "USAGE: " << argv[0] << " {play_file} {search_string...}" << endl;
        return 1;
    }
    ifstream play_file(argv[1]);
    if (!play_file) {
        cout << "Failed to open file " << argv[1] << endl;
        return 1;
    }
    string search_string = accumulate(argv + 2, argv + argc, string(), join(" "));
    string passage = find_dialog_passage(play_file, search_string);
    if (!passage.empty()) {
        cout << passage << endl;
    } else {
        cout << "Search term not found" << endl;
    }
    return 0;
}
