import sys

if len(sys.argv) != 7:
    print('arguments: <dataset path> <paper citation output> <paper name output> <author citation output> <author name output> <paper year output>')
    sys.exit(-1)


def write_out_paper_details(p_index, p_title, p_name_op, citations, citations_op, year, year_op):
    if p_index != 0:
        p_name_op.write('\n')
        citations_op.write('\n')
        year_op.write('\n')
    year_op.write(year)
    p_name_op.write(p_title)
    write_list_to_file(citations, citations_op)


def build_author_index_mapping(author_index, paper_index, author_list,
                               author_to_index, author_index_to_paper, author_op):
    for author in author_list:          # building mapping from author name to unique index
        if author not in author_to_index:
            author_to_index[author] = author_index
            author_index_to_paper[author_index] = []
            if author_index != 0:
                author_op.write('\n')
            author_op.write(author)
            author_index += 1
        papers = author_index_to_paper[author_to_index[author]]
        papers.append(paper_index)
    return author_index


def build_paper_author_index_mapping(paper_index, author_list, author_to_index, paper_to_author):
    if paper_index not in paper_to_author:
        paper_to_author[paper_index] = []
    authors = paper_to_author[paper_index]
    for author in author_list:
        authors.append(author_to_index[author])


def build_paper_citation_mapping(paper_index, citation_list, paper_to_cited_papers):
    if paper_index not in paper_to_cited_papers:
        paper_to_cited_papers[paper_index] = []
    cited = paper_to_cited_papers[paper_index]
    for citation in citation_list:
        cited.append(citation)


def build_author_author_citation_mapping(author_index_to_paper, paper_to_author, paper_to_cited_papers):
    author_to_collab = {}
    author_to_cited = {}
    for author in author_index_to_paper:            # for each author...
        if author not in author_to_collab:      # just init stuff
            author_to_collab[author] = []
        collaborators = author_to_collab[author]
        if author not in author_to_cited:
            author_to_cited[author] = []
        citations = author_to_cited[author]
        papers = author_index_to_paper[author]      # ..find the papers by that author
        for paper in papers:                        # for each paper by that author..
            authors = paper_to_author[paper]        # ..find the collaborators of that paper..
            for collab_author in authors:
                if collab_author != author:
                    collaborators.append(collab_author)     # and add collaborators other than author
            cited_papers = paper_to_cited_papers[paper]     # also, retrieve list of papers cited in authored paper
            for cited_paper in cited_papers:                # for each cited paper..
                cited_authors = paper_to_author[cited_paper]    # ..retrieve authors of said paper
                for cited_author in cited_authors:              # for each author of said cited paper
                    citations.append(cited_author)              # add author to citations list
    return author_to_collab, author_to_cited

def write_list_to_file(lst, op):
    comma = False
    for val in lst:
        if comma:
            op.write(',')
        else:
            comma = True
        op.write(str(val))


ip = open(sys.argv[1], 'r')
paper_paper_citations_op = open(sys.argv[2], 'w')
paper_name_op = open(sys.argv[3], 'w')
author_author_citations_op = open(sys.argv[4], 'w')
author_names_op = open(sys.argv[5], 'w')
paper_year_op = open(sys.argv[6], 'w')

author_to_index = {}             # mapping from academic to unique index
paper_to_author = {}          # mapping from paper index to academic indices
author_index_to_paper = {}
paper_to_cited_papers = {}

paper_index = 0
author_index = 0
author_list = None
citation_list = []
paper_title = None
paper_year = None
for line in ip:
    if len(line.strip()) == 0:  # end of a data block
        author_index = build_author_index_mapping(author_index, paper_index, author_list, author_to_index,
                                                  author_index_to_paper, author_names_op)
        build_paper_author_index_mapping(paper_index, author_list, author_to_index, paper_to_author)
        build_paper_citation_mapping(paper_index, citation_list, paper_to_cited_papers)
        # simply write out paper titles and paper citations
        write_out_paper_details(paper_index, paper_title, paper_name_op, citation_list, paper_paper_citations_op, paper_year, paper_year_op)
        author_list = None
        citation_list = []
        paper_title = None
        paper_index += 1
    elif line[:2] == '#*':      # paper name
        paper_title = line[2:].strip()
    elif line[:2] == '#@':      # list of authors
        author_list = line[2:].strip().split(',')
    elif line[:2] == '#%':      #
        citation_list.append(int(line[2:].strip()))
    elif line[:2] == '#t':
        paper_year = line[2:].strip()
author_to_collab, author_to_cited = build_author_author_citation_mapping(author_index_to_paper,
                                                                         paper_to_author, paper_to_cited_papers)
for author in range(0, author_index):
    if author != 0:
        author_author_citations_op.write('\n')
    collab = author_to_collab[author]
    write_list_to_file(collab, author_author_citations_op)
    author_author_citations_op.write('#')
    citations = author_to_cited[author]
    write_list_to_file(citations, author_author_citations_op)

ip.close()
paper_paper_citations_op.close()
paper_name_op.close()
author_author_citations_op.close()
author_names_op.close()
paper_year_op.close()
